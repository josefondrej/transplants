from abc import ABC, abstractmethod
from typing import List, Optional

from transplants.core.scorer.scorer_base import ScorerBase, TRANSPLANT_IMPOSSIBLE
from transplants.core.solution.matching import Matching
from transplants.core.solution.transplant import Transplant


class AdditiveScorerBase(ScorerBase, ABC):
    """Special scorer class that calculates the score of matching as sum of scores of its transplants
    If this is the case, then the optimal solution to the exchange problem can be found in polynomial time"""

    def __init__(self, forbidden_transplants: Optional[List[Transplant]] = None, min_required_base_score: float = 0.0):
        self._forbidden_transplants = forbidden_transplants or []
        self._min_required_base_score = min_required_base_score

    def score(self, matching: Matching) -> float:
        score = 0.0
        for chain in matching.chains:
            for transplant in chain.transplants:
                score += self.score_transplant(transplant=transplant)

        return score

    def score_transplant(self, transplant: Transplant) -> float:
        """Score transplant considering the results of score_transplant_base and the context of
            (1) explicitly forbidden transplants
            (2) minimal required score
            (3) requirement for better donor than his relatives for patients that have this specified
        """
        # Impossible if explicitly forbidden
        if transplant in self._forbidden_transplants:
            return TRANSPLANT_IMPOSSIBLE

        # Impossible if base score < min required score
        base_score = self.score_transplant_base(transplant)
        if base_score < self._min_required_base_score:
            return TRANSPLANT_IMPOSSIBLE

        # Impossible if recipient required better match than with all of his related donors
        if transplant.recipient.require_better_than_related_match:
            related_donors = transplant.recipient.related_donors
            potential_related_transplants = [Transplant(donor, transplant.recipient) for donor in related_donors]
            potential_possible_related_transplants = [transplant for transplant in potential_related_transplants
                                                      if transplant not in self._forbidden_transplants]
            potential_possible_related_transplant_scores = list(map(self.score_transplant_base,
                                                                    potential_possible_related_transplants))
            best_related_transplant_score = max(potential_possible_related_transplant_scores)
            if base_score < best_related_transplant_score:
                return TRANSPLANT_IMPOSSIBLE

        return base_score

    @abstractmethod
    def score_transplant_base(self, transplant: Transplant) -> float:
        """Score transplant as standalone operation without looking at context of the other patients
        or minimum required score"""
        pass
