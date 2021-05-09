from unittest import TestCase

from tests.test_utils.load_problem import load_problem
from transplants.problem.problem import Problem


class TestProblemSerialization(TestCase):
    def test_original_equals_deserialized_serialized(self):
        problem = load_problem()

        serialized_problem = Problem.to_dict(problem)
        deserialized_problem = Problem.from_dict(serialized_problem)

        self.assertEqual(problem, deserialized_problem)
