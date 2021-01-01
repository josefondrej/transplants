# Kidney exchange solver API
# Example Input:
#
# exchange_parameters = {
#     "patients": [
#         {'identifier': '435eb00', 'patient_type': 'recipient', 'medical_data': {'blood_type': {'type': '0', 'forbidden_types': ['A', 'AB', 'B']}, 'hla_system': {'antigens': {'B41', 'B53', 'DR13', 'A33', 'A66', 'DR8'}, 'antibodies': {'A1': None, 'A2': None, 'A3': None, 'A11': None, 'A24': None, 'A29': None, 'A30': None, 'A31': None, 'A32': None, 'A36': None, 'A43': None, 'A68': None, 'A69': None, 'A74': None, 'A80': None, 'B14': None, 'B64': None, 'B65': None, 'B46': None, 'B49': None, 'B50': None, 'B57': None, 'B58': None, 'Cw1': None, 'Cw3': None, 'Cw7': None, 'Cw8': None, 'DQ3': None, 'DQ7': None, 'DQ8': None, 'DQ9': None, 'DQ4': None, 'DQ5': None, 'DQ6': None}}}, 'related_donors': ['c17fb5b'], 'require_better_than_related_match': None},
#         {'identifier': '067eeb6', 'patient_type': 'recipient', 'medical_data': {'blood_type': {'type': '0', 'forbidden_types': ['A', 'AB', 'B']}, 'hla_system': {'antigens': {'B41', 'B63', 'A1', 'B62', 'A2', 'DR7', 'B15', 'DR11'}, 'antibodies': {'A24': None, 'A3': None, 'A32': None, 'A25': None, 'A11': None, 'A74': None, 'A34': None, 'A43': None, 'A66': None, 'A36': None, 'A26': None, 'A29': None, 'A31': None, 'A30': None, 'B63': None, 'B52': None, 'B58': None, 'B57': None, 'B51': None, 'B49': None, 'B59': None, 'B55': None, 'B13': None, 'B54': None, 'B42': None}}}, 'related_donors': ['3ad4cac'], 'require_better_than_related_match': None},
#         {'identifier': '7cb6d98', 'patient_type': 'recipient', 'medical_data': {'blood_type': {'type': '0', 'forbidden_types': ['A', 'AB', 'B']}, 'hla_system': {'antigens': {'B35', 'B37', 'A1', 'DR11', 'DR4'}, 'antibodies': {}}}, 'related_donors': ['78ee9c5'], 'require_better_than_related_match': None}
#     ],
#     "scorer": {
#         "type": "HLABloodTypeAdditiveScorer",
#         "compatible_blood_group_bonus": 10.0,
#         "incompatible_blood_group_malus": float("-inf"),
#         "hla_allele_compatibility_bonus": {"A": 1.0, "B": 3.0, "DRB1": 9.0},
#         "max_allowed_antibody_concentration": {"A1": 2000, "A2": 5000},
#         "forbidden_transplants": [("78ee9c5", "7cb6d98"), ("c17fb5b", "435eb00")],
#         "min_required_base_score": 0.0
#     },
#     "solver": {
#         "type": "ORToolsSolver"
#     }
# }

from typing import Dict

from transplants.api_utils.patients_from_params import patients_from_params
from transplants.api_utils.scorer_from_params import scorer_from_params
from transplants.api_utils.solver_from_params import solver_from_params
from transplants.core.solution.serialize_to_dict.matching import to_dict as matching_to_dict


def find_exchanges(exchange_parameters: Dict) -> Dict:
    serialized_patients = exchange_parameters["patients"]
    scorer_parameters = exchange_parameters["scorer"]
    solver_parameters = exchange_parameters["solver"]

    # Patients
    donors, recipients = patients_from_params(serialized_patients=serialized_patients)

    # Scorer
    scorer = scorer_from_params(scorer_parameters=scorer_parameters, patients=donors + recipients)

    # Solver
    solver = solver_from_params(solver_parameters=solver_parameters)

    matchings = solver.solve(
        donors=donors,
        recipients=recipients,
        scorer=scorer
    )

    solution = {
        "matchings": [matching_to_dict(matching) for matching in matchings]
    }

    return solution
