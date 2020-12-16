from transplants.core.scorer.scorer_base import ScorerBase
from transplants.core.solution.matching import Matching
from transplants.core.solution.transplant import Transplant


class AdditiveScorerBase(ScorerBase):
    def score(self, matching: Matching) -> float:
        score = 0.0
        for chain in matching.chains:
            for transplant in chain.pairs:
                score += self.score_transplant(transplant=transplant)

        return score

    def score_transplant(self, transplant: Transplant) -> float:
        raise NotImplementedError("Has to be overridden")
