from typing import Dict

from transplants.solver.or_tools_solver import ORToolsSolver
from transplants.solver.solver_base import SolverBase


def from_dict(dictionary: Dict) -> SolverBase:
    solver_type = dictionary["type"]
    if solver_type == "ORToolsSolver":
        solver = ORToolsSolver()
        return solver
    else:
        raise ValueError(f"Invalid solver type {solver_type} provided")
