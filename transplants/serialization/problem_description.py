from typing import Dict

from transplants.serialization.load_donors_recipients import load_donors_recipients
from transplants.serialization.scorer import from_dict as scorer_from_dict
from transplants.serialization.solver import from_dict as solver_from_dict
from transplants.find_solution.problem_description import ProblemDescription


def from_dict(dictionary: Dict) -> ProblemDescription:
    serialized_patients = dictionary["patients"]
    serialized_scorer = dictionary["scorer"]
    serialized_solver = dictionary["solver"]

    donors, recipients = load_donors_recipients(serialized_patients=serialized_patients)
    scorer = scorer_from_dict(dictionary=serialized_scorer)
    solver = solver_from_dict(dictionary=serialized_solver)

    problem_description = ProblemDescription(patients=donors + recipients, scorer=scorer, solver=solver)
    return problem_description
