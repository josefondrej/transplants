from abc import ABC, abstractmethod
from typing import List

import numpy as np

from transplants.problem.patient.donor import Donor
from transplants.problem.patient.recipient import Recipient
from transplants.problem.problem import Problem
from transplants.solver.scorer.scorer_base import ScorerBase
from transplants.solution.matching import Matching
from transplants.solution.solution import Solution
from transplants.solution.transplant import Transplant
from transplants.solver.find_chains import get_arguments_from_transplant_matrix_and_patients, find_chains, \
    index_chains_to_patient_chains


class SolverBase(ABC):
    """Base class for solver"""

    def __init__(self, scorer: ScorerBase):
        self._scorer = scorer

    @abstractmethod
    def solve(self, problem: Problem) -> Solution:
        """ Return list of scored matchings sorted by their .score"""
        pass

    @staticmethod
    def get_matching_from_transplant_matrix(transplant_matrix: np.ndarray, problem: Problem) -> Matching:
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
            problem=problem
        )
        index_chains = find_chains(edges=edges)
        patient_chains = index_chains_to_patient_chains(
            index_chains=index_chains,
            vertex_to_patient=vertex_to_patient
        )
        return Matching(chains=patient_chains)

    def get_score_matrix(self, donors: List[Donor], recipients: List[Recipient]) -> np.ndarray:
        score_matrix = [
            [self._scorer.score_transplant(Transplant(donor_id=donor.identifier, recipient_id=recipient.identifier))
             for recipient in recipients]
            for donor in donors]
        return np.array(score_matrix)
