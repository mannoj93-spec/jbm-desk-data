// Inspect only this deployment job and this run attempt. Never cancel another deployment.
function isCollision(annotation) {
  return annotation.annotation_level === 'failure' &&
    /Failed to create deployment \(status: 400\)/.test(annotation.message || '') &&
    /due to in progress deployment\./.test(annotation.message || '') &&
    /first or wait for it to complete\./.test(annotation.message || '');
}

async function classify({github, context, core, sleep = ms => new Promise(r => setTimeout(r, ms))}) {
  const jobs = await github.paginate(github.rest.actions.listJobsForWorkflowRunAttempt, {
    ...context.repo, run_id: context.runId, attempt_number: Number(process.env.GITHUB_RUN_ATTEMPT), per_page: 100,
  });
  const job = jobs.filter(j => j.name === 'deploy' && j.status === 'in_progress');
  if (job.length !== 1) throw new Error('Cannot identify the current deployment job');
  const checkRunId = Number(new URL(job[0].check_run_url).pathname.split('/').pop());
  if (!Number.isSafeInteger(checkRunId) || checkRunId <= 0) throw new Error('Invalid deployment check ID');
  for (let i = 0; i < 3; i++) {
    const annotations = await github.paginate(github.rest.checks.listAnnotations, {
      ...context.repo, check_run_id: checkRunId, per_page: 100,
    });
    if (annotations.some(isCollision)) {
      core.info('Pages creation collided with an existing deployment; waiting 45 seconds before one retry.');
      await sleep(45000);
      return true;
    }
    if (i < 2) await sleep(10000); // bounded allowance for annotation publication
  }
  return false; // Unclassified failures remain failures, including permissions/artifact errors.
}

module.exports = {isCollision, classify};
