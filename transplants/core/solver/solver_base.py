from abc import ABC, abstractmethod
from typing import List, Set

import numpy as np

from transplants.core.patient.donor import Donor
from transplants.core.patient.recipient import Recipient
from transplants.core.scorer.additive_scorer_base import AdditiveScorerBase
from transplants.core.scorer.scorer_base import ScorerBase
from transplants.core.solution.matching import Matching
from transplants.core.solution.transplant import Transplant
from transplants.core.solver.find_chains import get_arguments_from_transplant_matrix_and_patients, find_chains, \
    index_chains_to_patient_chains


class SolverBase(ABC):
    """Base class for solver"""

    @abstractmethod
    def solve(self, donors: Set[Donor], recipients: Set[Recipient], scorer: ScorerBase) -> List[Matching]:
        """ Return list of scored matchings sorted by their .score"""
        pass

    @staticmethod
    def get_matching_from_transplant_matrix(transplant_matrix: np.ndarray, donors: List[Donor],
                                            recipients: List[Recipient]) -> Matching:
        """Get Matching from transplant matrix

        Args:
            transplant_matrix (np.array(int64)): can have values 0 / 1
                transplant_matrix[i,j] = 1 means transplant from donor i to recipient j is performed
                transplant_matrix[i,j] = 0 means transplant from donor i to recipient j is NOT performed
            donors: list of donors in the exact ordering that corresponds to the transplant matrix
            recipients: list of recipients in the exact ordering that corresponds to the transplant matrix

        Returns: Matching containing the patients
        """
        edges, vertex_to_patient = get_arguments_from_transplant_matrix_and_patients(
            transplant_matrix=transplant_matrix,
            donors=donors,
            recipients=recipients
        )
        index_chains = find_chains(edges=edges)
        patient_chains = index_chains_to_patient_chains(
            index_chains=index_chains,
            vertex_to_patient=vertex_to_patient
        )
        return Matching(chains=patient_chains)

    @staticmethod
    def get_score_matrix(donors: List[Donor], recipients: List[Recipient], scorer: AdditiveScorerBase) -> np.ndarray:
        score_matrix = [[scorer.score_transplant(Transplant(donor=donor, recipient=recipient))
                         for recipient in recipients]
                        for donor in donors]
        return np.array(score_matrix)
