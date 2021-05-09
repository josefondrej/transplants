from tests.test_utils.default_ids import SOLVER_CONFIG_ID
from transplants.model.solver_config import SolverConfig


def load_solver_config(solver_config_id: str = SOLVER_CONFIG_ID):
    solver_config = SolverConfig(
        solver_config_id=solver_config_id,
        solver_name="ORToolsSolver",
        parameters={
            "scorer_parameters": {
                "compatible_blood_group_bonus": 0.0,
            }
        }
    )

    return solver_config
