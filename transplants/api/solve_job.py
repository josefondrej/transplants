from datetime import datetime

from marshmallow import fields

from transplants.api.job import Job
from transplants.api.solve import solve
from transplants.model.problem import Problem
from transplants.model.solver_config import SolverConfig


def serialize_datetime(timestamp: datetime):
    serialized_timestamp = fields.DateTime().serialize("dt", {"dt": timestamp})
    return serialized_timestamp


def solve_job(job_id: str) -> str:
    job = Job.find_by_id(job_id)

    if job.solution_id is not None:
        return job.solution_id

    problem_id, solver_config_id = job.problem_id, job.solver_config_id
    problem = Problem.find_by_id(problem_id)
    solver_config = SolverConfig.find_by_id(solver_config_id)

    if problem is None:
        raise AssertionError(f"Problem is None for job_id={job_id}")

    if solver_config is None:
        raise AssertionError(f"SolverConfig is None for job_id={job_id}")

    job.update_db(solution_start_timestamp=serialize_datetime(datetime.now()))

    solution = solve(problem=problem, solver_config=solver_config)
    solution.save_to_db()

    job.update_db(solution_id=solution.solution_id)
    job.update_db(solution_end_timestamp=serialize_datetime(datetime.now()))

    return solution.solution_id
