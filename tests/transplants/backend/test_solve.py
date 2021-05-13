from unittest import TestCase

from tests.test_utils.load_job import load_job
from tests.test_utils.load_problem import load_problem
from tests.test_utils.load_solution import load_solution
from tests.test_utils.load_solver_config import load_solver_config
from transplants.api.solve import solve
from transplants.api.solve_job import solve_job
from transplants.database.mongo_db import initialize_db, kidney_exchange_database
from transplants.database.purge_db import purge_db
from transplants.model.solution import Solution


class TestSolve(TestCase):

    def test_solve(self):
        problem = load_problem()
        solver_config = load_solver_config()
        expected_solution = load_solution()

        solution = solve(problem=problem, solver_config=solver_config)

        print(solution.to_dict())
        print(expected_solution.to_dict())

        self.assertEqual(solution, expected_solution)

    def test_solve_db(self):
        initialize_db(kidney_exchange_database)
        purge_db(kidney_exchange_database)

        problem = load_problem()
        solver_config = load_solver_config()
        job = load_job()

        problem.save_to_db()
        solver_config.save_to_db()
        job.save_to_db()

        solution_id = solve_job(job.job_id)
        solution = Solution.find_by_id(solution_id)

        expected_solution = load_solution()

        self.assertEqual(solution, expected_solution)
