from datetime import datetime

from tests.test_utils.load_job import load_job
from tests.test_utils.load_problem import load_problem
from tests.test_utils.load_solution import load_solution
from tests.test_utils.load_solver_config import load_solver_config
from tests.test_utils.mock_db import MockDB
from transplants.api.solve_job import serialize_datetime
from transplants.model.problem import Problem
from transplants.model.solution import Solution
from transplants.model.solver_config import SolverConfig


class TestDatabase(MockDB):
    def test_load_save_problem(self):
        problem = load_problem()
        problem_id = problem.problem_id

        problem.save_to_db()
        retrieved_problem = Problem.find_by_id(identifier=problem_id)
        self.assertEqual(problem, retrieved_problem)

    def test_load_save_solution(self):
        solution = load_solution()
        solution_id = solution.solution_id

        solution.save_to_db()
        retrieved_solution = Solution.find_by_id(identifier=solution_id)
        self.assertEqual(solution, retrieved_solution)

    def test_load_save_solver_config(self):
        solver_config = load_solver_config()
        solver_config_id = solver_config.solver_config_id

        solver_config.save_to_db()
        retrieved_solver_config = SolverConfig.find_by_id(identifier=solver_config_id)
        self.assertEqual(solver_config, retrieved_solver_config)

    def test_update_job_datetime(self):
        job = load_job()
        job.save_to_db()
        timestamp = datetime.now()
        job.update_db(solution_start_timestamp=serialize_datetime(timestamp))
        job = job.find_by_id(job.job_id)
        self.assertEqual(timestamp, job.solution_start_timestamp)
