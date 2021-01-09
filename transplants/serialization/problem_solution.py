from typing import Dict

from transplants.find_solution.problem_solution import ProblemSolution
from transplants.serialization.matching import to_dict as matching_to_dict


def to_dict(problem_solution: ProblemSolution) -> Dict:
    dictionary = {"matchings": [matching_to_dict(matching) for matching in problem_solution.matchings]}
    return dictionary
