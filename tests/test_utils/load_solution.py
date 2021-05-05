from tests.test_utils.default_ids import PROBLEM_ID, SOLVER_CONFIG_ID
from transplants.solution.solution import Solution


def load_solution(problem_id: str = PROBLEM_ID, solver_config_id: str = SOLVER_CONFIG_ID, solution_id: str = None):
    if solution_id is None:
        solution_id = f"{problem_id}_{solver_config_id}"

    solution_serialized = {
        "problem_id": problem_id,
        "solver_config_id": solver_config_id,
        "solution_id": solution_id,

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

    return Solution.from_dict(solution_serialized)
