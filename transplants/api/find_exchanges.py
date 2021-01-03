# Kidney exchange solver API

from typing import Dict

from transplants.api_utils.patients_from_params import patients_from_params
from transplants.api_utils.scorer_from_params import scorer_from_params
from transplants.api_utils.solver_from_params import solver_from_params
from transplants.core.solution.serialize_to_dict.matching import to_dict as matching_to_dict


def find_exchanges(exchange_parameters: Dict) -> Dict:
    """Get the best kidney exchanges given exchange parameters

    Args:
        exchange_parameters: Dictionary describing the patients, scorer and solver used to get the solution
        Example:
            {'patients': [
                {'identifier': 'a1b3398', 'patient_type': 'donor', 'country': 'CZE', 'medical_data': {'hla_system': {'antigens': ['A11', 'A26', 'B62', 'B38', 'DR4', 'DR11', 'DR53', 'DR52', 'DQ7', 'DQ8', 'DP2', 'DP10', 'Cw9', 'Cw12'], 'antibodies': {}}, 'blood_type': {'type': 'A', 'forbidden_types': None}}},
                {'identifier': '300ffe8', 'patient_type': 'donor', 'country': 'CZE', 'medical_data': {'hla_system': {'antigens': ['A1', 'A68', 'B8', 'B53', 'DR9', 'DR13', 'DR53', 'DR52', 'DQ9', 'DQ6'], 'antibodies': {}}, 'blood_type': {'type': '0', 'forbidden_types': None}}},
                {'identifier': '1959daa', 'patient_type': 'donor', 'country': 'CZE', 'medical_data': {'hla_system': {'antigens': ['A11', 'B62', 'B46', 'DR9', 'DR15', 'DR53', 'DR51', 'DQ9', 'DQ5'], 'antibodies': {}}, 'blood_type': {'type': 'B', 'forbidden_types': None}}},
                ...
                {'identifier': '7cb6d98', 'patient_type': 'recipient', 'related_donors': ['78ee9c5'], 'country': 'AUT', 'medical_data': {'hla_system': {'antigens': ['A1', 'B35', 'B37', 'DR4', 'DR11'], 'antibodies': {}}, 'blood_type': {'type': '0', 'forbidden_types': ['A', 'AB', 'B']}}}
                ],
            'solver': {
                'type': 'ORToolsSolver'
                },
            'scorer': {
                'type': 'HLABloodTypeAdditiveScorer',
                'compatible_blood_group_bonus': 0.0,
                'incompatible_blood_group_malus': -inf,
                'hla_allele_compatibility_bonus': {'A': 1.0, 'B': 3.0, 'DRB1': 9.0},
                'max_allowed_antibody_concentration': {},
                'forbidden_transplants': [],
                'min_required_base_score': 0.0
                }
            }


    Returns:
        Dictionary describing the patient matching(s) in the exchange(s)
        These can optionally contain scores
        If there is more than one exchange outputted then the order is from the best to the worst exchange
        Example:
            {
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
    """
    serialized_patients = exchange_parameters["patients"]
    scorer_parameters = exchange_parameters["scorer"]
    solver_parameters = exchange_parameters["solver"]

    # Patients
    donors, recipients = patients_from_params(serialized_patients=serialized_patients)

    # Scorer
    scorer = scorer_from_params(scorer_parameters=scorer_parameters, patients=donors + recipients,
                                add_related_to_forbidden=True)

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
