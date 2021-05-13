import json
from typing import Dict

from tests.test_utils.default_ids import PROBLEM_ID, SOLVER_CONFIG_ID
from transplants.model.solution import Solution
from transplants.utils.paths import get_abs_path


def load_solution_serialized(problem_id: str = PROBLEM_ID, solver_config_id: str = SOLVER_CONFIG_ID,
                             solution_id: str = None) -> Dict:
    if solution_id is None:
        solution_id = f"{problem_id}_{solver_config_id}"

    solution_example_path = get_abs_path("tests/test_utils/solution_example.json")
    with open(solution_example_path, "r") as file:
        solution_serialized = json.load(file)

        solution_serialized["problem_id"] = problem_id
        solution_serialized["solver_config_id"] = solver_config_id
        solution_serialized["solution_id"] = solution_id

    return solution_serialized


def load_solution(problem_id: str = PROBLEM_ID, solver_config_id: str = SOLVER_CONFIG_ID, solution_id: str = None):
    solution_serialized = load_solution_serialized(problem_id=problem_id, solver_config_id=solver_config_id,
                                                   solution_id=solution_id)
    return Solution.from_dict(solution_serialized)
