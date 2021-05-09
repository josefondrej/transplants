from tests.test_utils.default_ids import JOB_ID, PROBLEM_ID, SOLVER_CONFIG_ID
from transplants.api.job import Job


def load_job(job_id: str = JOB_ID, problem_id: str = PROBLEM_ID, solver_config_id: str = SOLVER_CONFIG_ID) -> Job:
    job = Job(
        job_id=job_id,
        problem_id=problem_id,
        solver_config_id=solver_config_id
    )

    return job
