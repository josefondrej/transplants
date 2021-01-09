import json
from unittest import TestCase

from transplants.serialization.matching import standardize_matching_dict_representation
from transplants.utils.find_exchanges import find_exchanges


class TestFindExchanges(TestCase):

    def test_or_tools_solver(self):
        patients_data_path = "./test/test_utils/patient_pool_example.json"

        with open(patients_data_path, "r") as patients_data_file:
            serialized_patients = json.load(patients_data_file)

        scorer_parameters = {
            "type": "HLABloodTypeAdditiveScorer",
            "compatible_blood_group_bonus": 0.0,
            "incompatible_blood_group_malus": float("-inf"),
            "hla_allele_compatibility_bonus": {"A": 1.0, "B": 3.0, "DRB1": 9.0},
            "max_allowed_antibody_concentration": {},
            "forbidden_transplants": [],
            "min_required_base_score": 0.0
        }

        solver_parameters = {
            "type": "ORToolsSolver"
        }

        exchange_parameters = {
            "patients": serialized_patients,
            "solver": solver_parameters,
            "scorer": scorer_parameters
        }

        expected_exchanges = {
            'matchings': [
                {'chains': [
                    {'transplants': [
                        {'donor': '07c54b8', 'recipient': 'dfa96d8', 'score': 17.0},
                        {'donor': '180effe', 'recipient': 'd39b597', 'score': 36.0},
                        {'donor': 'dbc9028', 'recipient': '7cb6d98', 'score': 2.0},
                        {'donor': '78ee9c5', 'recipient': 'fd2fee8', 'score': 1.0},
                        {'donor': '7e4427f', 'recipient': '15fe2d9', 'score': 20.0},
                        {'donor': 'c999a2c', 'recipient': '26fe98e', 'score': 36.0}
                    ], 'is_cycle': False, 'score': 112.0},
                    {'transplants': [
                        {'donor': '826a39c', 'recipient': '03f543f', 'score': 13.0},
                        {'donor': '3567fde', 'recipient': '4394ac9', 'score': 25.0}
                    ], 'is_cycle': False, 'score': 38.0}
                ], 'score': 150.0}
            ]
        }

        calculated_exchanges = find_exchanges(exchange_problem_parameters=exchange_parameters)

        # WARN! Here we sort the chains in the matching which is required to use assertDictEqual later on
        for exchange in [expected_exchanges, calculated_exchanges]:
            for matching in exchange["matchings"]:
                standardize_matching_dict_representation(matching)

        print(expected_exchanges)
        print(calculated_exchanges)

        self.assertDictEqual(expected_exchanges, calculated_exchanges)
