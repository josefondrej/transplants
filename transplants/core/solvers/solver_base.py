from typing import List

from transplants.core.patients.donor import Donor
from transplants.core.patients.recipient import Recipient
from transplants.core.scored_matching import ScoredMatching
from transplants.core.scorers.scorer_base import ScorerBase


class SolverBase:
    def solve(self, donors: List[Donor], recipients: List[Recipient], scorer: ScorerBase) -> List[ScoredMatching]:
        raise NotImplementedError("Has to be overriden")
