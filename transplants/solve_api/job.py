from datetime import datetime

from marshmallow import fields

from transplants.database.database_mixin import DatabaseMixin
from transplants.database.mongo_db import job_collection
from transplants.serialization.serialization_mixin import SerializationMixin, add_marshmallow_schema, \
    serializable_property


@add_marshmallow_schema
class Job(SerializationMixin, DatabaseMixin):
    id_name = "job_id"
    collection = job_collection

    def __init__(self, job_id: str, problem_id: str, solver_config_id: str,
                 solution_id: str = None,
                 submission_timestamp: datetime = None,
                 solution_start_timestamp: datetime = None,
                 solution_end_timestamp: datetime = None):
        self._job_id = job_id
        self._problem_id = problem_id
        self._solver_config_id = solver_config_id
        self._solution_id = solution_id
        self._submission_timestamp = submission_timestamp
        self._solution_start_timestamp = solution_start_timestamp
        self._solution_end_timestamp = solution_end_timestamp

    def __eq__(self, other):
        if not isinstance(other, Job):
            return False

        return (self.job_id == other.job_id) and \
               (self.problem_id == other.problem_id) and \
               (self.solver_config_id == other.solver_config_id) and \
               (self.solution_id == other.solution_id) and \
               (self.submission_timestamp == other.submission_timestamp) and \
               (self.solution_start_timestamp == other.solution_end_timestamp) and \
               (self.solution_end_timestamp == other.solution_end_timestamp)

    def __hash__(self):
        return hash((self.job_id, self.problem_id, self.solver_config_id, self.solution_id,
                     str(self.submission_timestamp), str(self.solution_timestamp)))

    @serializable_property(fields.Str())
    def job_id(self) -> str:
        return self._job_id

    @serializable_property(fields.Str())
    def problem_id(self) -> str:
        return self._problem_id

    @serializable_property(fields.Str())
    def solver_config_id(self) -> str:
        return self._solver_config_id

    @serializable_property(fields.Str(allow_none=True, required=False))
    def solution_id(self) -> str:
        return self._solution_id

    @serializable_property(fields.DateTime(allow_none=True, required=False))
    def submission_timestamp(self) -> datetime:
        return self._submission_timestamp

    @serializable_property(fields.DateTime(allow_none=True, required=False))
    def solution_start_timestamp(self) -> datetime:
        return self._solution_start_timestamp

    @serializable_property(fields.DateTime(allow_none=True, required=False))
    def solution_end_timestamp(self) -> datetime:
        return self._solution_end_timestamp
