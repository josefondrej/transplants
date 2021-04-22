from unittest import TestCase

from tests.test_utils.load_problem import load_problem
from transplants.marshmallow_schemas import ProblemSchema


class TestProblem(TestCase):
    def test_original_equals_deserialized_serialized(self):
        problem = load_problem()
        problem_schema = ProblemSchema()
        serialized_problem = problem_schema.dump(problem)
        deserialized_problem = problem_schema.load(serialized_problem)
        self.assertEqual(problem, deserialized_problem)