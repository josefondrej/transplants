from transplants.problem.problem import Problem
from transplants.solution.solution import Solution
from transplants.solver.scorer.default_forbidden_transplants import get_default_forbidden_transplants
from transplants.solver.solver_config import SolverConfig
from transplants.solver.solver_factory import build_solver


def _inject_default_forbidden_transplants_to_config(solver_config: SolverConfig, problem: Problem):
    default_forbidden_transplants = get_default_forbidden_transplants(problem.patients)
    solver_config.append_values_to_list_parameter("forbidden_transplants", default_forbidden_transplants)


def solve(problem: Problem, solver_config: SolverConfig) -> Solution:
    """Calculate solution to Kidney Exchange Problem
    Args:
        problem: The kidney exchange problem
        solver_config: Description of the method used for finding the solution
    """
    _inject_default_forbidden_transplants_to_config(solver_config=solver_config, problem=problem)

    solver = build_solver(solver_config=solver_config)
    solution = solver.solve(problem=problem)

    solution._solution_id = problem.problem_id + "_" + solver_config.solver_config_id
    solution._problem_id = problem.problem_id
    solution._solver_config_id = solver_config.solver_config_id

    return solution
