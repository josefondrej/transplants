from tests.test_utils.default_ids import JOB_ID, PROBLEM_ID, SOLVER_CONFIG_ID
from transplants.model.job import Job


def load_job_serialized(job_id: str = JOB_ID, problem_id: str = PROBLEM_ID, solver_config_id: str = SOLVER_CONFIG_ID):
    job_serialized = dict(
        job_id=job_id,
        problem_id=problem_id,
        solver_config_id=solver_config_id
    )
    return job_serialized


def load_job(job_id: str = JOB_ID, problem_id: str = PROBLEM_ID, solver_config_id: str = SOLVER_CONFIG_ID) -> Job:
    job_serialized = load_job_serialized(job_id=job_id, problem_id=problem_id, solver_config_id=solver_config_id)
    job = Job.from_dict(job_serialized)

    return job
