import logging
from typing import Set, List

import numpy as np
from ortools.linear_solver.pywraplp import Solver, Variable

from transplants.patient.donor import Donor
from transplants.patient.recipient import Recipient
from transplants.scorer.additive_scorer_base import AdditiveScorerBase
from transplants.scorer.scorer_base import TRANSPLANT_IMPOSSIBLE
from transplants.solution.matching import Matching
from transplants.solver.solver_base import SolverBase


class ORToolsSolver(SolverBase):
    """Solver using Google's MIP library

    For more details see:
        - https://developers.google.com/optimization/mip/integer_opt
    """

    @staticmethod
    def _create_transplant_indicators(solver: Solver, donor_to_recipient_scores: np.ndarray) -> np.ndarray:
        donor_to_recipient_transplant_performed = np.zeros_like(donor_to_recipient_scores, dtype="object")
        donor_count, recipient_count = donor_to_recipient_scores.shape
        for i in range(donor_count):
            for j in range(recipient_count):
                if donor_to_recipient_scores[i, j] != TRANSPLANT_IMPOSSIBLE:
                    donor_to_recipient_transplant_performed[i, j] = solver.BoolVar(f"{i} -> {j}")

        donor_to_recipient_scores[donor_to_recipient_scores == TRANSPLANT_IMPOSSIBLE] = 1
        return donor_to_recipient_transplant_performed

    @staticmethod
    def _get_solution_value(variable_array: np.ndarray) -> np.ndarray:
        solution_value = np.zeros_like(variable_array)
        for i, row in enumerate(variable_array):
            for j, item in enumerate(row):
                if isinstance(item, Variable):
                    value = item.solution_value()
                else:
                    value = item

                solution_value[i, j] = value

        return solution_value

    def solve(self, donors: Set[Donor], recipients: Set[Recipient], scorer: AdditiveScorerBase) -> List[Matching]:
        donors, recipients = list(donors), list(recipients)
        transplant_score_matrix = SolverBase.get_score_matrix(donors=donors, recipients=recipients, scorer=scorer)
        i_to_donor = dict(enumerate(donors))
        donor_to_i = {value: key for key, value in i_to_donor.items()}

        j_to_recipient = dict(enumerate(recipients))

        j_to_related_i = {j: [donor_to_i[donor] for donor in recipient.related_donors]
                          for j, recipient in j_to_recipient.items()}

        solver = Solver.CreateSolver("GLOP")
        transplant_indicator_matrix = ORToolsSolver._create_transplant_indicators(
            solver=solver,
            donor_to_recipient_scores=transplant_score_matrix
        )

        # 1. Each donor can give at most one kidney
        for x_row in transplant_indicator_matrix:
            solver.Add(x_row.sum() <= 1)

        # 2. Each recipient can get at most one kidney
        for x_col in transplant_indicator_matrix.T:
            solver.Add(x_col.sum() <= 1)

        # 3. Number of kidneys donated by recipient's related donor(s) <= number of kidneys recipient receives
        for j, i_vec in j_to_related_i.items():
            solver.Add(transplant_indicator_matrix[i_vec, :].sum() <= transplant_indicator_matrix.T[j].sum())

        # Define optimized function
        solver.Maximize((transplant_score_matrix * transplant_indicator_matrix).sum())

        status = solver.Solve()

        if status == Solver.OPTIMAL:
            transplant_matrix = ORToolsSolver._get_solution_value(transplant_indicator_matrix)
            transplant_matrix = transplant_matrix.astype("int64")
            matching = SolverBase.get_matching_from_transplant_matrix(
                transplant_matrix=transplant_matrix,
                donors=donors,
                recipients=recipients
            )
            matchings = [matching]
        else:
            logging.error("No solution found")
            matchings = []

        for matching in matchings:
            scorer.score(matching)

        return matchings
