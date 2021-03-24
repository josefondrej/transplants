from transplants.solver.solver_config import SolverConfig


def load_solver_config():
    return SolverConfig(
        solver_config_id="test_solver_config",
        solver_name="ORToolsSolver",
        parameters={
            "scorer_parameters": {
                "compatible_blood_group_bonus": 0.0,
            }
        }
    )
