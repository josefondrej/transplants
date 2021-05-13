from abc import ABC

import numpy as np

from transplants.backend.scorer.additive_scorer_base import AdditiveScorerBase
from transplants.backend.solver_base import SolverBase
from transplants.model.problem import Problem
from transplants.model.transplant import Transplant


class AdditiveSolverBase(SolverBase, ABC):
    """Solver which finds patient matchings with the best score. The matching score is calculated using
    an instance of AdditiveScorerBase"""

    def __init__(self, scorer: AdditiveScorerBase):
        self._scorer = scorer

    def get_score_matrix(self, problem: Problem) -> np.ndarray:
        score_matrix = [
            [self._scorer.score_transplant(
                Transplant(donor_id=donor.patient_id, recipient_id=recipient.patient_id),
                problem=problem
            )
                for recipient in problem.recipients]
            for donor in problem.donors]
        return np.array(score_matrix)
