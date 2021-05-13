import logging

import numpy as np
from ortools.linear_solver.pywraplp import Solver, Variable

from transplants.backend.additive_solver_base import AdditiveSolverBase
from transplants.backend.matching_from_matrix import get_matching_from_transplant_matrix
from transplants.backend.scorer.additive_scorer_base import AdditiveScorerBase
from transplants.backend.scorer.hla_blood_type_additive_scorer import HLABloodTypeAdditiveScorer
from transplants.backend.scorer.scorer_base import TRANSPLANT_IMPOSSIBLE
from transplants.model.problem import Problem
from transplants.model.solution import Solution
from transplants.model.solver_config import SolverConfig


class ORToolsSolver(AdditiveSolverBase):
    """Solver using Google's MIP library

    For more details see:
        - https://developers.google.com/optimization/mip/integer_opt
    """

    def __init__(self, scorer: AdditiveScorerBase):
        super().__init__(scorer=scorer)

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

    def solve(self, problem: Problem) -> Solution:
        donors, recipients = problem.donors, problem.recipients
        transplant_score_matrix = self.get_score_matrix(problem=problem)
        i_to_donor = dict(enumerate(donors))
        donor_id_to_i = {donor.patient_id: i for i, donor in i_to_donor.items()}

        j_to_recipient = dict(enumerate(recipients))

        j_to_related_i = {j: [donor_id_to_i[donor_id] for donor_id in recipient.related_donor_ids]
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
            matching = get_matching_from_transplant_matrix(
                transplant_matrix=transplant_matrix,
                problem=problem
            )
            matchings = [matching]
        else:
            logging.error("No solution found")
            matchings = []

        for matching in matchings:
            self._scorer.score(matching, problem=problem)

        return Solution(
            solution_id=None,
            problem_id=problem.problem_id,
            solver_config_id=None,
            matchings=matchings
        )

    @classmethod
    def build_from_config(cls, config: SolverConfig) -> "ORToolsSolver":
        scorer_parameters = config.parameters["scorer_parameters"]
        scorer = HLABloodTypeAdditiveScorer(**scorer_parameters)
        return ORToolsSolver(scorer=scorer)
