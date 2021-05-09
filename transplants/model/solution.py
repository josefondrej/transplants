from typing import List

from marshmallow import fields

from transplants.database.database_mixin import DatabaseMixin
from transplants.database.mongo_db import solution_collection
from transplants.model.matching import Matching
from transplants.serialization.serialization_mixin import SerializationMixin, add_marshmallow_schema, \
    serializable_property


@add_marshmallow_schema
class Solution(SerializationMixin, DatabaseMixin):
    id_name = "solution_id"
    collection = solution_collection

    """
    Args:
        solution_id: Unique identifier of the solution
        problem_id: Unique identifier of the model this solution solves
        matchings: Ordered list of patient matchings that solve the model
    """

    def __init__(self, solution_id: str, problem_id: str, solver_config_id: str, matchings: List[Matching]):
        self._solution_id = solution_id
        self._problem_id = problem_id
        self._solver_config_id = solver_config_id
        self._matchings = matchings

    def __eq__(self, other):
        if not isinstance(other, Solution):
            return False

        if self.solution_id != other.solution_id:
            return False

        if self.problem_id != other.problem_id:
            return False

        return self.matchings == other.matchings

    def __hash__(self):
        return hash((self._solution_id, self._problem_id, tuple(matching for matching in self.matchings)))

    @serializable_property(fields.String())
    def solution_id(self):
        return self._solution_id

    @serializable_property(fields.String())
    def problem_id(self) -> str:
        return self._problem_id

    @serializable_property(fields.String())
    def solver_config_id(self) -> str:
        return self._solver_config_id

    @serializable_property(fields.List(fields.Nested(Matching.marshmallow_schema)))
    def matchings(self) -> List[Matching]:
        return self._matchings
