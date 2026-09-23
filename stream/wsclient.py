"""Minimal RFC 6455 WebSocket client (standard library only).

Supports wss:// and ws://, an optional HTTP CONNECT proxy (HTTPS_PROXY / https_proxy, used only
when set), text and binary frames, fragmentation, ping/pong and close. One reader, one writer
lock. Timeouts are enforced with socket timeouts; `recv` returns None on timeout so the caller
can run its heartbeat logic.
"""
import base64
import hashlib
import os
import select
import socket
import ssl
import struct
import threading
import urllib.parse

GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
OP_CONT, OP_TEXT, OP_BIN, OP_CLOSE, OP_PING, OP_PONG = 0x0, 0x1, 0x2, 0x8, 0x9, 0xA
MAX_MESSAGE = 16 * 1024 * 1024
FRAME_STALL_S = 30.0


class WSClosed(Exception):
    pass


def encode_frame(opcode, payload, mask=True, fin=True):
    head = bytes([(0x80 if fin else 0) | opcode])
    n = len(payload)
    mbit = 0x80 if mask else 0
    if n < 126:
        head += bytes([mbit | n])
    elif n < 65536:
        head += bytes([mbit | 126]) + struct.pack("!H", n)
    else:
        head += bytes([mbit | 127]) + struct.pack("!Q", n)
    if not mask:
        return head + payload
    key = os.urandom(4)
    return head + key + bytes(b ^ key[i % 4] for i, b in enumerate(payload))


def _read_exact(sock, n):
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise WSClosed("connection closed by peer")
        buf += chunk
    return buf


def read_frame(sock):
    """Returns (fin, opcode, payload). Raises socket.timeout if nothing arrives in time."""
    b0, b1 = _read_exact(sock, 2)
    fin, opcode = bool(b0 & 0x80), b0 & 0x0F
    masked, n = bool(b1 & 0x80), b1 & 0x7F
    if n == 126:
        n = struct.unpack("!H", _read_exact(sock, 2))[0]
    elif n == 127:
        n = struct.unpack("!Q", _read_exact(sock, 8))[0]
    if n > MAX_MESSAGE:
        raise WSClosed(f"frame of {n} bytes exceeds the limit")
    key = _read_exact(sock, 4) if masked else None
    data = _read_exact(sock, n) if n else b""
    if key:
        data = bytes(b ^ key[i % 4] for i, b in enumerate(data))
    return fin, opcode, data


class WebSocket:
    def __init__(self, url, timeout=10.0, proxy=None, headers=None):
        self.url = url
        u = urllib.parse.urlparse(url)
        self.secure = u.scheme == "wss"
        self.host, self.port = u.hostname, u.port or (443 if self.secure else 80)
        self.path = (u.path or "/") + (f"?{u.query}" if u.query else "")
        self.timeout = timeout
        self.proxy = proxy if proxy is not None else (os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy"))
        self.headers = headers or {}
        self.sock = None
        self.lock = threading.Lock()
        self._frag = None

    def connect(self):
        if self.proxy:
            p = urllib.parse.urlparse(self.proxy)
            raw = socket.create_connection((p.hostname, p.port or 80), timeout=self.timeout)
            auth = ""
            if p.username:
                token = base64.b64encode(f"{urllib.parse.unquote(p.username)}:{urllib.parse.unquote(p.password or '')}".encode()).decode()
                auth = f"Proxy-Authorization: Basic {token}\r\n"
            raw.sendall(f"CONNECT {self.host}:{self.port} HTTP/1.1\r\nHost: {self.host}:{self.port}\r\n{auth}\r\n".encode())
            resp = b""
            while b"\r\n\r\n" not in resp:
                chunk = raw.recv(4096)
                if not chunk:
                    raise WSClosed("proxy closed the connection")
                resp += chunk
            status = resp.split(b"\r\n")[0]
            if b" 200" not in status:
                raise WSClosed(f"proxy refused CONNECT: {status[:80]!r}")
        else:
            raw = socket.create_connection((self.host, self.port), timeout=self.timeout)
        if self.secure:
            ctx = ssl.create_default_context(cafile=os.environ.get("SSL_CERT_FILE") or None)
            raw = ctx.wrap_socket(raw, server_hostname=self.host)
        key = base64.b64encode(os.urandom(16)).decode()
        extra = "".join(f"{k}: {v}\r\n" for k, v in self.headers.items())
        raw.sendall((f"GET {self.path} HTTP/1.1\r\nHost: {self.host}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n"
                     f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\nUser-Agent: jbm-stream/1\r\n{extra}\r\n").encode())
        resp = b""
        while b"\r\n\r\n" not in resp:
            chunk = raw.recv(4096)
            if not chunk:
                raise WSClosed("closed during handshake")
            resp += chunk
        head, _, rest = resp.partition(b"\r\n\r\n")
        status = head.split(b"\r\n")[0]
        if b" 101" not in status:
            raise WSClosed(f"handshake refused: {status[:120]!r}")
        accept = base64.b64encode(hashlib.sha1((key + GUID).encode()).digest()).decode()
        if accept.encode() not in head:
            raise WSClosed("bad Sec-WebSocket-Accept")
        if rest:
            raise WSClosed("unexpected data after handshake")
        self.sock = raw
        return self

    def send_text(self, text):
        with self.lock:
            self.sock.sendall(encode_frame(OP_TEXT, text.encode()))

    def recv(self, timeout=None):
        """Next complete text/binary message as str/bytes, or None when nothing arrives within
        `timeout`. Waiting uses select() so a timeout never interrupts a frame half-way; once a
        frame has started, a stall longer than FRAME_STALL_S is a broken connection (WSClosed)."""
        wait = timeout if timeout is not None else self.timeout
        while True:
            pending = getattr(self.sock, "pending", lambda: 0)()
            if not pending and not select.select([self.sock], [], [], wait)[0]:
                return None
            self.sock.settimeout(FRAME_STALL_S)
            try:
                fin, op, data = read_frame(self.sock)
            except (socket.timeout, TimeoutError):
                raise WSClosed("frame stalled mid-read")
            if op == OP_PING:
                with self.lock:
                    self.sock.sendall(encode_frame(OP_PONG, data))
                continue
            if op == OP_PONG:
                continue
            if op == OP_CLOSE:
                raise WSClosed("close frame received")
            if op in (OP_TEXT, OP_BIN):
                if fin:
                    return data.decode() if op == OP_TEXT else data
                self._frag = [op, data]
                continue
            if op == OP_CONT and self._frag is not None:
                self._frag[1] += data
                if len(self._frag[1]) > MAX_MESSAGE:
                    raise WSClosed("fragmented message too large")
                if fin:
                    op0, payload = self._frag
                    self._frag = None
                    return payload.decode() if op0 == OP_TEXT else payload
                continue
            raise WSClosed(f"unexpected opcode {op}")

    def close(self):
        try:
            if self.sock:
                with self.lock:
                    self.sock.sendall(encode_frame(OP_CLOSE, b""))
        except OSError:
            pass
        try:
            if self.sock:
                self.sock.close()
        finally:
            self.sock = None
