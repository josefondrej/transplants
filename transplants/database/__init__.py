from transplants.database.inject_database_methods import inject_database_methods
from transplants.database.mongo_db import solution_collection, problem_collection, solver_config_collection
from transplants.problem.problem import Problem
from transplants.solution.solution import Solution
from transplants.solver.solver_config import SolverConfig

inject_database_methods(model_class=Solution, collection=solution_collection, id_name="solution_id")
inject_database_methods(model_class=Problem, collection=problem_collection, id_name="problem_id")
inject_database_methods(model_class=SolverConfig, collection=solver_config_collection, id_name="solver_config_id")
