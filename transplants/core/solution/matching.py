from typing import Set

from transplants.core.solution.chain import Chain
from transplants.core.solution.scored_mixin import ScoredMixin


class Matching(ScoredMixin):
    """Set of several transplant chains which can be either cycles or sequences"""

    def __init__(self, chains: Set[Chain]):
        self._chains = chains

    @property
    def chains(self) -> Set[Chain]:
        return self._chains
