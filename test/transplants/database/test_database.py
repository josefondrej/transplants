from unittest import TestCase

from test.test_utils.load_problem import load_problem
from test.test_utils.load_solution import load_solution
from test.test_utils.load_solver_config import load_solver_config
from transplants.database.mongo_db import kidney_exchange_database, initialize_db
from transplants.database.purge_db import purge_db
from transplants.problem.problem import Problem
from transplants.solution.solution import Solution
from transplants.solver.solver_config import SolverConfig


class TestDatabase(TestCase):
    purge_db(database=kidney_exchange_database)
    initialize_db(database=kidney_exchange_database)

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
