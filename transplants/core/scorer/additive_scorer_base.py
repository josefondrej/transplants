from abc import ABC, abstractmethod

from transplants.core.scorer.scorer_base import ScorerBase
from transplants.core.solution.matching import Matching
from transplants.core.solution.transplant import Transplant


class AdditiveScorerBase(ScorerBase, ABC):
    """Special scorer class that calculates the score of matching as sum of scores of its transplants
    If this is the case, then the optimal solution to the exchange problem can be found in polynomial time"""

    def score(self, matching: Matching) -> float:
        score = 0.0
        for chain in matching.chains:
            for transplant in chain.pairs:
                score += self.score_transplant(transplant=transplant)

        return score

    @abstractmethod
    def score_transplant(self, transplant: Transplant) -> float:
        pass
