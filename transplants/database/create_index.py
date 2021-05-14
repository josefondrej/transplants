from typing import List

from pymongo.database import Database

from transplants.database.database_mixin import DatabaseMixin
from transplants.model import Patient
from transplants.model.job import Job
from transplants.model.problem import Problem
from transplants.model.solution import Solution
from transplants.model.solver_config import SolverConfig

_registered_classes: List[DatabaseMixin] = [Problem, Solution, SolverConfig, Job, Patient]


def create_db_indices(database: Database):
    for cls in _registered_classes:
        collection = database.get_collection(cls.db_collection_name)
        collection.create_index(cls.db_id_name, unique=True)
