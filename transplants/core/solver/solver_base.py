from typing import List, Set

from transplants.core.patient.donor import Donor
from transplants.core.patient.recipient import Recipient
from transplants.core.scorer.scorer_base import ScorerBase
from transplants.core.solution.matching import Matching


class SolverBase:
    def solve(self, donors: Set[Donor], recipients: Set[Recipient], scorer: ScorerBase) -> List[Matching]:
        """ Return list of scored matchings sorted by their .score"""
        raise NotImplementedError("Has to be overridden")
