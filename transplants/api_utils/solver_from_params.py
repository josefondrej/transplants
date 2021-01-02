from typing import Dict

from transplants.core.solver.or_tools_solver import ORToolsSolver
from transplants.core.solver.solver_base import SolverBase


def solver_from_params(solver_parameters: Dict) -> SolverBase:
    solver_type = solver_parameters["type"]
    if solver_type == "ORToolsSolver":
        solver = ORToolsSolver()
        return solver
    else:
        raise ValueError(f"Invalid solver type {solver_type} provided")
