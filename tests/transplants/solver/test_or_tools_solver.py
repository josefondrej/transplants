import json
from pprint import pprint
from unittest import TestCase

from transplants.marshmallow_schemas.problem.problem_schema import ProblemSchema as ProblemSchema
from transplants.marshmallow_schemas.solution.solution_schema import SolutionSchema as SolutionSchema
from transplants.solver.or_tools_solver import ORToolsSolver
from transplants.solver.scorer.default_forbidden_transplants import get_default_forbidden_transplants
from transplants.solver.scorer.hla_blood_type_additive_scorer import HLABloodTypeAdditiveScorer
from transplants.utils.paths import get_abs_path


class TestFindExchanges(TestCase):
    def setUp(self) -> None:
        patients_data_path = get_abs_path("tests/test_utils/patient_pool_example.json")

        with open(patients_data_path, "r") as patients_data_file:
            serialized_patients = json.load(patients_data_file)

        self.problem_schema = ProblemSchema()
        self.solution_schema = SolutionSchema()

        self.solution_id = "test_solution_id"
        self.problem_id = "test_problem_id"
        self.solver_config_id = "test_solver_config_id"

        self.problem_serialized = {
            "problem_id": self.problem_id,
            "patients": serialized_patients
        }
        self.problem = self.problem_schema.load(self.problem_serialized)

        self.expected_solution_serialized = {
            "solution_id": self.solution_id,
            "problem_id": self.problem_id,
            "solver_config_id": self.solver_config_id,
            "matchings": [
                {"chains": [
                    {"transplants": [
                        {"donor": "07c54b8", "recipient": "dfa96d8", "score": 17.0},
                        {"donor": "180effe", "recipient": "d39b597", "score": 36.0},
                        {"donor": "dbc9028", "recipient": "7cb6d98", "score": 2.0},
                        {"donor": "78ee9c5", "recipient": "fd2fee8", "score": 1.0},
                        {"donor": "7e4427f", "recipient": "15fe2d9", "score": 20.0},
                        {"donor": "c999a2c", "recipient": "26fe98e", "score": 36.0}
                    ], "is_cycle": False, "score": 112.0},
                    {"transplants": [
                        {"donor": "826a39c", "recipient": "03f543f", "score": 13.0},
                        {"donor": "3567fde", "recipient": "4394ac9", "score": 25.0}
                    ], "is_cycle": False, "score": 38.0}
                ], "score": 150.0}
            ]
        }
        self.expected_solution = self.solution_schema.load(self.expected_solution_serialized)

        self.forbidden_transplants = get_default_forbidden_transplants(patients=self.problem.patients)

        self.scorer = HLABloodTypeAdditiveScorer(
            compatible_blood_group_bonus=0.0,
            forbidden_transplants=self.forbidden_transplants
        )

    def test_or_tools_solver(self):
        solver = ORToolsSolver(scorer=self.scorer)

        calculated_solution = solver.solve(problem=self.problem)
        calculated_solution._solution_id = self.solution_id

        calculated_solution_serialized = self.solution_schema.dump(calculated_solution)

        pprint(calculated_solution_serialized)
        pprint(self.expected_solution_serialized)

        self.assertEqual(calculated_solution, self.expected_solution)

        # This won't work since the items in the ["matchings"]["chains"] might be in different order
        # and assertDictEqual can't handle this
        # self.assertDictEqual(calculated_solution_serialized, expected_solution_serialized)
