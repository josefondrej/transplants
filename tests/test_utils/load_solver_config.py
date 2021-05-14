from typing import Dict

from tests.test_utils.default_ids import SOLVER_CONFIG_ID
from transplants.model.solver_config import SolverConfig


def load_solver_config_serialized(solver_config_id: str = SOLVER_CONFIG_ID) -> Dict:
    solver_config_serialized = dict(
        solver_config_id=solver_config_id,
        solver_name="ORToolsSolver",
        parameters={
            "scorer_parameters": {
                "compatible_blood_group_bonus": 0.0,
            }
        })

    return solver_config_serialized


def load_solver_config(solver_config_id: str = SOLVER_CONFIG_ID) -> SolverConfig:
    solver_config_serialized = load_solver_config_serialized(solver_config_id=solver_config_id)
    solver_config = SolverConfig.from_dict(solver_config_serialized)

    return solver_config
