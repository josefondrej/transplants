from transplants.backend.or_tools_solver import ORToolsSolver
from transplants.backend.solver_base import SolverBase
from transplants.model.solver_config import SolverConfig

registered_solvers = [ORToolsSolver]

_solver_name_to_solver_constructor = {solver_constructor.__name__: solver_constructor
                                      for solver_constructor in registered_solvers}


def build_solver(solver_config: SolverConfig) -> SolverBase:
    solver_constructor = _solver_name_to_solver_constructor.get(solver_config.solver_name)
    if solver_constructor is None:
        raise ValueError(f"Invalid SolverConfig(solver_name={solver_config.solver_name})")

    solver = solver_constructor.build_from_config(config=solver_config)
    return solver
