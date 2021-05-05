from unittest import TestCase

from tests.test_utils.load_solution import load_solution
from transplants.solution.solution import Solution


class TestSolution(TestCase):
    def test_original_equals_deserialized_serialized(self):
        solution = load_solution()
        solution_schema = Solution.marshmallow_schema()

        serialized_solution = solution_schema.dump(solution)
        deserialized_solution = solution_schema.load(serialized_solution)

        self.assertEqual(solution, deserialized_solution)
