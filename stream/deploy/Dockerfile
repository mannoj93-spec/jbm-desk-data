# JBM streaming collector - standard library only, no third-party packages.
# Build from the repository root:  docker build -f stream/deploy/Dockerfile -t jbm-stream:1.0 .
FROM python:3.11-slim
RUN useradd --system --uid 10001 jbm && mkdir -p /var/lib/jbm-stream && chown jbm /var/lib/jbm-stream
WORKDIR /opt/jbm
COPY stream/ /opt/jbm/stream/
USER jbm
ENV PYTHONUNBUFFERED=1 STREAM_DATA_DIR=/var/lib/jbm-stream
VOLUME ["/var/lib/jbm-stream"]
HEALTHCHECK --interval=60s --timeout=10s --start-period=90s \
  CMD python -m stream.check_heartbeat /var/lib/jbm-stream --max-age 60 --max-down 120 || exit 1
CMD ["python", "-m", "stream.service", "--config", "/opt/jbm/stream/config.json"]
