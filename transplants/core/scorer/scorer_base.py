from transplants.core.solution.matching import Matching


class ScorerBase:
    def score(self, matching: Matching) -> float:
        raise NotImplementedError("Has to be overridden")
