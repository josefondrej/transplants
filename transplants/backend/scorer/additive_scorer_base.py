from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from transplants.backend.scorer.scorer_base import ScorerBase, TRANSPLANT_IMPOSSIBLE
from transplants.model.chain import Chain
from transplants.model.matching import Matching
from transplants.model.problem import Problem
from transplants.model.scored_mixin import assign_result_to_argument
from transplants.model.transplant import Transplant


class AdditiveScorerBase(ScorerBase, ABC):
    """
    Special scorer class that calculates the score of matching as sum of scores of its transplants
    If this is the case, then the optimal solution to the exchange model can be found in polynomial time

    Args:
        forbidden_transplants: Transplants that we explicitly do not allow represented by Tuple[donor.id, recipient.id].
            BEWARE: These should usually be all transplants (related donor, recipient) for recipients that have
            require_better_than_related_match = False, however this has to be explicitly specified!
        min_required_base_score: If the result of the score_transplant_base function is less than this value,
            we score the transplant as impossible
    """

    def __init__(self, forbidden_transplants: Optional[List[Tuple[str, str]]] = None,
                 min_required_base_score: float = 0.0):
        self._forbidden_transplants = forbidden_transplants or []
        self._min_required_base_score = min_required_base_score

    @assign_result_to_argument
    def score(self, matching: Matching, problem: Problem) -> float:
        score = 0.0
        for chain in matching.chains:
            score += self.score_chain(chain, problem)

        return score

    @assign_result_to_argument
    def score_chain(self, chain: Chain, problem: Problem) -> float:
        score = 0.0
        for transplant in chain.transplants:
            score += self.score_transplant(transplant, problem)

        return score

    @assign_result_to_argument
    def score_transplant(self, transplant: Transplant, problem: Problem) -> float:
        """Score transplant considering the results of score_transplant_base and the context of
            (1) explicitly forbidden transplants
            (2) minimal required score
            (3) requirement for better donor than his relatives for patients that have this specified
        """
        donor = problem.get_patient(transplant.donor_id)
        recipient = problem.get_patient(transplant.recipient_id)

        # Impossible if explicitly forbidden
        if (donor.patient_id, recipient.patient_id) in self._forbidden_transplants:
            return TRANSPLANT_IMPOSSIBLE

        # Impossible if base score < min required score
        base_score = self.score_transplant_base(transplant, problem)
        if base_score < self._min_required_base_score:
            return TRANSPLANT_IMPOSSIBLE

        # Impossible if recipient required better match than with all of his related donors
        if recipient.require_better_than_related_match:
            related_donors = transplant.recipient.related_donor_ids
            potential_related_transplants = [Transplant(donor.patient_id, transplant.recipient.patient_id)
                                             for donor in related_donors]
            potential_possible_related_transplants = [transplant for transplant in potential_related_transplants
                                                      if transplant not in self._forbidden_transplants]
            potential_possible_related_transplant_scores = [self.score_transplant_base(transplant, problem)
                                                            for transplant in potential_possible_related_transplants]
            best_related_transplant_score = max(potential_possible_related_transplant_scores)
            if base_score < best_related_transplant_score:
                return TRANSPLANT_IMPOSSIBLE

        return base_score

    @abstractmethod
    def score_transplant_base(self, transplant: Transplant, problem: Problem) -> float:
        """Score transplant as standalone operation without looking at context of the other patients
        or minimum required score"""
        pass
