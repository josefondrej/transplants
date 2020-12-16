from abc import ABC
from typing import List

from transplants.core.solution.scored_mixin import ScoredMixin
from transplants.core.solution.transplant import Transplant


class Chain(ABC, ScoredMixin):
    """General base class for chain of transplants"""

    def __init__(self, pairs: List[Transplant], is_cycle: bool = None):
        self._pairs = pairs
        self._is_cycle = is_cycle

    @property
    def pairs(self) -> List[Transplant]:
        return self._pairs

    @property
    def is_cycle(self) -> bool:
        return self._is_cycle
