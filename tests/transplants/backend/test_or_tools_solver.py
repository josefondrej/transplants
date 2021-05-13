from pprint import pprint
from unittest import TestCase

from tests.test_utils.load_problem import load_problem
from tests.test_utils.load_solution import load_solution_serialized
from transplants.backend.or_tools_solver import ORToolsSolver
from transplants.backend.scorer.default_forbidden_transplants import get_default_forbidden_transplants
from transplants.backend.scorer.hla_blood_type_additive_scorer import HLABloodTypeAdditiveScorer
from transplants.model.solution import Solution


class TestFindExchanges(TestCase):
    def setUp(self) -> None:
        self.solution_id = "test_solution_id"
        self.problem_id = "test_problem_id"
        self.solver_config_id = "test_solver_config_id"

        self.problem = load_problem(problem_id=self.problem_id)

        self.expected_solution_serialized = load_solution_serialized(solution_id=self.solution_id,
                                                                     solver_config_id=self.solver_config_id,
                                                                     problem_id=self.problem_id)
        self.expected_solution = Solution.from_dict(self.expected_solution_serialized)

        self.forbidden_transplants = get_default_forbidden_transplants(patients=self.problem.patients)

        self.scorer = HLABloodTypeAdditiveScorer(
            compatible_blood_group_bonus=0.0,
            forbidden_transplants=self.forbidden_transplants
        )

    def test_or_tools_solver(self):
        solver = ORToolsSolver(scorer=self.scorer)

        calculated_solution = solver.solve(problem=self.problem)
        calculated_solution._solution_id = self.solution_id

        calculated_solution_serialized = Solution.to_dict(calculated_solution)

        pprint(calculated_solution_serialized)
        pprint(self.expected_solution_serialized)

        self.assertEqual(calculated_solution, self.expected_solution)

        # This won't work since the items in the ["matchings"]["chains"] might be in different order
        # and assertDictEqual can't handle this
        # self.assertDictEqual(calculated_solution_serialized, expected_solution_serialized)
