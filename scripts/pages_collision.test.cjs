const {test} = require('node:test');
const assert = require('node:assert/strict');
const {isCollision, classify} = require('./pages_collision.cjs');
const collision = {annotation_level:'failure', message:'Failed to create deployment (status: 400) with build version abc. Responded with: Deployment request failed for abc due to in progress deployment. Please cancel def first or wait for it to complete.'};
test('only the known Pages creation collision is retryable', () => {
  assert.equal(isCollision(collision), true);
  for (const change of [{annotation_level:'warning'}, {message:'in progress deployment'},
    {message:collision.message.replace('400','403')}, {message:'Artifact invalid'},
    {message:'Timeout reached, aborting!'}]) assert.equal(isCollision({...collision,...change}), false);
});
function fixture(annotations, jobs) {
  const calls=[], waits=[];
  process.env.GITHUB_RUN_ATTEMPT='2';
  return {calls, waits, args:{context:{repo:{owner:'o',repo:'r'},runId:123},core:{info(){}},
    sleep:async ms=>waits.push(ms), github:{rest:{actions:{listJobsForWorkflowRunAttempt:'jobs'},checks:{listAnnotations:'annotations'}},
      paginate:async (method,args)=>{calls.push([method,args]);return method==='jobs'
        ? jobs ?? [{name:'deploy',status:'in_progress',check_run_url:'https://api.github.com/repos/o/r/check-runs/42'}]
        : annotations;}}}};
}
test('observed collision waits once and scopes lookup to current attempt and deployment check', async()=>{
  const f=fixture([collision]);assert.equal(await classify(f.args),true);
  assert.deepEqual(f.waits,[45000]);assert.equal(f.calls[0][1].attempt_number,2);
  assert.equal(f.calls[1][1].check_run_id,42);
});
test('missing or other errors are bounded and never turn into a retry',async()=>{
  const f=fixture([]);assert.equal(await classify(f.args),false);
  assert.deepEqual(f.waits,[10000,10000]);assert.equal(f.calls.length,4);
});
test('ambiguous jobs fail closed',async()=>{
  await assert.rejects(classify(fixture([],[]).args),/Cannot identify/);
});
