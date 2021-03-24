from transplants.marshmallow_schemas import SolutionSchema


def load_solution():
    solution_serialized = {
        "solution_id": "test_problem_test_solver_config",
        "solver_config_id": "test_solver_config",
        "problem_id": "test_problem",
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

    solution_schema = SolutionSchema()
    return solution_schema.load(solution_serialized)
