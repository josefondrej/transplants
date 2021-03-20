from unittest import TestCase

from test.test_utils.load_solution import load_solution
from transplants.marshmallow_schemas import SolutionSchema


class TestSolution(TestCase):
    def test_original_equals_deserialized_serialized(self):
        solution = load_solution()
        solution_schema = SolutionSchema()

        serialized_solution = solution_schema.dump(solution)
        deserialized_solution = solution_schema.load(serialized_solution)

        self.assertEqual(solution, deserialized_solution)
