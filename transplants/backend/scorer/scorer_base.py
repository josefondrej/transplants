from abc import ABC, abstractmethod

from transplants.model.matching import Matching
from transplants.model.problem import Problem

TRANSPLANT_IMPOSSIBLE = float("-inf")


class ScorerBase(ABC):
    """Most general scorer class that assigns some value to patient matching
    The larger the value, the better the matching is"""

    @abstractmethod
    def score(self, matching: Matching, problem: Problem) -> float:
        raise NotImplementedError("Has to be overridden")
