from typing import Set

from transplants.solution.chain import Chain
from transplants.solution.scored_mixin import ScoredMixin


class Matching(ScoredMixin):
    """Set of several transplant chains which can be either cycles or sequences"""

    def __init__(self, chains: Set[Chain]):
        self._chains = chains

    def __eq__(self, other):
        if not isinstance(other, Matching):
            return False

        return set(self.chains) == set(other.chains)

    def __hash__(self):
        ordered_chains = sorted(self.chains, key=hash)
        return hash(tuple(hash(chain) for chain in ordered_chains))

    @property
    def chains(self) -> Set[Chain]:
        return self._chains