from typing import Dict

from transplants.find_solution.problem_description import ProblemDescription
from transplants.find_solution.problem_solution import ProblemSolution
from transplants.serialization.problem_description import from_dict as problem_description_from_dict
from transplants.serialization.problem_solution import to_dict as problem_solution_to_dict


def find_solution(problem_description: ProblemDescription) -> ProblemSolution:
    matchings = problem_description.solver.solve(
        donors=problem_description.donors,
        recipients=problem_description.recipients,
        scorer=problem_description.scorer
    )

    solution = ProblemSolution(matchings=matchings)
    return solution


def find_solution_serialized(serialized_problem_description: Dict) -> Dict:
    """Get the best kidney exchanges given exchange parameters"""
    problem_description = problem_description_from_dict(serialized_problem_description)
    solution = find_solution(problem_description)
    return problem_solution_to_dict(solution)
