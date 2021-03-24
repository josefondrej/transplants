from abc import ABC

import numpy as np

from transplants.problem.problem import Problem
from transplants.solution.transplant import Transplant
from transplants.solver.scorer.additive_scorer_base import AdditiveScorerBase
from transplants.solver.solver_base import SolverBase


class AdditiveSolverBase(SolverBase, ABC):
    """Solver which finds patient matchings with the best score. The matching score is calculated using
    an instance of AdditiveScorerBase"""

    def __init__(self, scorer: AdditiveScorerBase):
        self._scorer = scorer

    def get_score_matrix(self, problem: Problem) -> np.ndarray:
        score_matrix = [
            [self._scorer.score_transplant(
                Transplant(donor_id=donor.identifier, recipient_id=recipient.identifier),
                problem=problem
            )
                for recipient in problem.recipients]
            for donor in problem.donors]
        return np.array(score_matrix)
