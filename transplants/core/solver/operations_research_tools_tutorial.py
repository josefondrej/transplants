import numpy as np
from ortools.linear_solver import pywraplp
from ortools.linear_solver.pywraplp import Solver

from test.load_test_patient_pool import load_donors_recipients
from transplants.core.scorer.hla_blood_type_additive_scorer import HLABloodTypeAdditiveScorer
from transplants.core.scorer.scorer_base import TRANSPLANT_IMPOSSIBLE
from transplants.core.solution.transplant import Transplant


def _create_transplant_indicators(solver: Solver, donor_to_recipient_scores: np.ndarray) -> np.ndarray:
    donor_to_recipient_transplant_performed = np.zeros_like(donor_to_recipient_scores, dtype="object")
    W_row_count, W_col_count = donor_to_recipient_scores.shape
    for i in range(W_row_count):
        for j in range(W_col_count):
            if donor_to_recipient_scores[i, j] != TRANSPLANT_IMPOSSIBLE:
                donor_to_recipient_transplant_performed[i, j] = solver.BoolVar(f"{i} -> {j}")

    donor_to_recipient_scores[donor_to_recipient_scores == TRANSPLANT_IMPOSSIBLE] = 1
    return donor_to_recipient_transplant_performed


def main():
    scorer = HLABloodTypeAdditiveScorer()
    donors, recipients = load_donors_recipients(data_path="../../../test/test_patient_pool.json")

    i_to_donor = dict(enumerate(donors))
    j_to_recipient = dict(enumerate(recipients))
    donor_to_i = {value: key for key, value in i_to_donor.items()}
    recipient_to_j = {value: key for key, value in j_to_recipient.items()}
    j_to_related_i = {j: [donor_to_i[donor] for donor in recipient.related_donors]
                      for j, recipient in j_to_recipient.items()}

    W = np.array(
        [[scorer.score_transplant(Transplant(donor=donor, recipient=recipient)) for recipient in recipients]
         for donor in donors]
    )

    solver = Solver.CreateSolver("GLOP")
    X = _create_transplant_indicators(solver=solver, donor_to_recipient_scores=W)

    # Define constraints
    # 1. Each donor can give at most one kidney
    for x_row in X:
        solver.Add(x_row.sum() <= 1)

    # 2. Each recipient can get at most one kidney
    for x_col in X.T:
        solver.Add(x_col.sum() <= 1)

    # 3. Number of kidneys donated by recipient's related donor(s) <= number of kidneys recipient receives
    for j, i_vec in j_to_related_i.items():
        solver.Add(X[i_vec, :].sum() <= X.T[j].sum())

    # Define optimized function
    solver.Maximize((W * X).sum())

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        print('Objective value =', solver.Objective().Value())
        print('x =', X)

    else:
        print('The problem does not have an optimal solution.')

    print('\nAdvanced usage:')
    print('Problem solved in %f milliseconds' % solver.wall_time())
    print('Problem solved in %d iterations' % solver.iterations())
    print('Problem solved in %d branch-and-bound nodes' % solver.nodes())


if __name__ == '__main__':
    main()
