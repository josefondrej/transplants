from datetime import datetime


class Job:
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

    @property
    def job_id(self) -> str:
        return self._job_id

    @property
    def problem_id(self) -> str:
        return self._problem_id

    @property
    def solver_config_id(self) -> str:
        return self._solver_config_id

    @property
    def solution_id(self) -> str:
        return self._solution_id

    @property
    def submission_timestamp(self) -> datetime:
        return self._submission_timestamp

    @property
    def solution_start_timestamp(self) -> datetime:
        return self._solution_start_timestamp

    @property
    def solution_end_timestamp(self) -> datetime:
        return self._solution_end_timestamp
