from unittest import TestCase

from test.test_utils.load_problem import load_problem
from test.test_utils.load_solution import load_solution
from test.test_utils.load_solver_config import load_solver_config
from transplants.database.mongo_db import initialize_db, kidney_exchange_database
from transplants.database.purge_db import purge_db
from transplants.solution.solution import Solution
from transplants.solve import solve, solve_db


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
        expected_solution = load_solution()

        problem.save_to_db()
        solver_config.save_to_db()

        solution_id = solve_db(problem_id=problem.problem_id, solver_config_id=solver_config.solver_config_id)
        solution = Solution.find_by_id(solution_id)

        self.assertEqual(solution, expected_solution)
