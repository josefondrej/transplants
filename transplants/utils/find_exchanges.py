from typing import Dict

from transplants.serialization.matching import to_dict as matching_to_dict
from transplants.serialization.scorer import from_dict as scorer_from_dict
from transplants.serialization.solver import from_dict as solver_from_dict
from transplants.utils.load_donors_recipients import load_donors_recipients


def find_exchanges(exchange_problem_parameters: Dict) -> Dict:
    """Get the best kidney exchanges given exchange parameters

    Args:
        add_related_to_forbidden: this should
    """
    serialized_patients = exchange_problem_parameters["patients"]
    serialized_scorer = exchange_problem_parameters["scorer"]
    serialized_solver = exchange_problem_parameters["solver"]

    donors, recipients = load_donors_recipients(serialized_patients=serialized_patients)
    scorer = scorer_from_dict(dictionary=serialized_scorer)

    solver = solver_from_dict(dictionary=serialized_solver)

    matchings = solver.solve(
        donors=donors,
        recipients=recipients,
        scorer=scorer
    )

    solution = {"matchings": [matching_to_dict(matching) for matching in matchings]}

    return solution
