from unittest import TestCase

from transplants.marshmallow_schemas.solution.chain_schema import ChainSchema
from transplants.marshmallow_schemas.solution.matching_schema import MatchingSchema
from transplants.marshmallow_schemas.solution.solution_schema import SolutionSchema
from transplants.marshmallow_schemas.solution.transplant_schema import TransplantSchema


class TestSolutionSchema(TestCase):
    def test_serialize_deserialize(self):
        transplant_serialized = {"donor": "07c54b8", "recipient": "dfa96d8", "score": 17.0}

        chain_one_serialized = {"transplants": [
            {"donor": "07c54b8", "recipient": "dfa96d8", "score": 17.0},
            {"donor": "180effe", "recipient": "d39b597", "score": 36.0},
            {"donor": "dbc9028", "recipient": "7cb6d98", "score": 2.0},
            {"donor": "78ee9c5", "recipient": "fd2fee8", "score": 1.0},
            {"donor": "7e4427f", "recipient": "15fe2d9", "score": 20.0},
            {"donor": "c999a2c", "recipient": "26fe98e", "score": 36.0}
        ], "is_cycle": False, "score": 112.0}

        chain_two_serialized = {"transplants": [
            {"donor": "826a39c", "recipient": "03f543f", "score": 13.0},
            {"donor": "3567fde", "recipient": "4394ac9", "score": 25.0}
        ], "is_cycle": False, "score": 38.0}

        matching_serialized = {"chains": [chain_one_serialized, chain_two_serialized], "score": 150.0}

        solution_serialized = {
            "solution_id": "test_solution_id",
            "problem_id": "test_problem_id",
            "solver_config_id": "test_solver_config_id",
            "matchings": [matching_serialized]
        }

        transplant_schema = TransplantSchema()
        chain_schema = ChainSchema()
        matching_schema = MatchingSchema()
        solution_schema = SolutionSchema()

        self.assertDictEqual(transplant_serialized,
                             transplant_schema.dump(transplant_schema.load(transplant_serialized)))

        self.assertDictEqual(chain_one_serialized, chain_schema.dump(chain_schema.load(chain_one_serialized)))
        self.assertDictEqual(chain_two_serialized, chain_schema.dump(chain_schema.load(chain_two_serialized)))

        self.assertDictEqual(matching_serialized, matching_schema.dump(matching_schema.load(matching_serialized)))

        self.assertDictEqual(solution_serialized, solution_schema.dump(solution_schema.load(solution_serialized)))

    def test_assert_dict_equals_works_as_expected(self):
        self.assertDictEqual({"X": {"A": 1, "B": 2}}, {"X": {"B": 2, "A": 1}})
