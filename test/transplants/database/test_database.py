import os
from unittest import TestCase

from test.test_utils.load_problem import load_problem
from test.test_utils.load_solution import load_solution
from transplants.database.mongo_db import KIDNEY_EXCHANGE_DATABASE_NAME_ENV_VAR_NAME, \
    TEST_KIDNEY_EXCHANGE_DATABASE_NAME
from transplants.problem.problem import Problem
from transplants.solution.solution import Solution


class TestDatabase(TestCase):
    def setUp(self) -> None:
        os.environ[KIDNEY_EXCHANGE_DATABASE_NAME_ENV_VAR_NAME] = TEST_KIDNEY_EXCHANGE_DATABASE_NAME

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
