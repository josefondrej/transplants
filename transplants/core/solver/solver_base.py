from abc import ABC, abstractmethod
from typing import List, Set

from transplants.core.patient.donor import Donor
from transplants.core.patient.recipient import Recipient
from transplants.core.scorer.scorer_base import ScorerBase
from transplants.core.solution.matching import Matching


class SolverBase(ABC):
    """Base class for solver"""

    @abstractmethod
    def solve(self, donors: Set[Donor], recipients: Set[Recipient], scorer: ScorerBase) -> List[Matching]:
        """ Return list of scored matchings sorted by their .score"""
        pass
