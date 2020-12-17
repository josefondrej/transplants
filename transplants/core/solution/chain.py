from abc import ABC
from typing import List

from transplants.core.solution.scored_mixin import ScoredMixin
from transplants.core.solution.transplant import Transplant


class Chain(ABC, ScoredMixin):
    """General base class for chain of transplants"""

    def __init__(self, transplants: List[Transplant], is_cycle: bool = None):
        self._transplants = transplants
        self._is_cycle = is_cycle

    @property
    def transplants(self) -> List[Transplant]:
        return self._transplants

    @property
    def is_cycle(self) -> bool:
        return self._is_cycle
