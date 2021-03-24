from typing import List

from transplants.solution.matching import Matching


class Solution:
    """Contains information about the solution
    and the method that was used to find it

    Args:
        solution_id: Unique identifier of the solution
        problem_id: Unique identifier of the problem this solution solves
        matchings: Ordered list of patient matchings that solve the problem
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
        return hash((self._solution_id, self._problem_id, tuple(hash(matching) for matching in self.matchings)))

    @property
    def solution_id(self):
        return self._solution_id

    @property
    def problem_id(self) -> str:
        return self._problem_id

    @property
    def solver_config_id(self) -> str:
        return self._solver_config_id

    @property
    def matchings(self) -> List[Matching]:
        return self._matchings
