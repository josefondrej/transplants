# Good start on Mixed Integer Programming with Google's OR Tools can be found at
# https://developers.google.com/optimization/mip/integer_opt
from typing import List, Dict, Optional

import numpy as np
from ortools.linear_solver import pywraplp
from ortools.linear_solver.pywraplp import Solver, Variable
from pip._vendor.colorama import Fore

from test.load_test_patient_pool import load_donors_recipients
from transplants.core.scorer.hla_blood_type_additive_scorer import HLABloodTypeAdditiveScorer
from transplants.core.scorer.scorer_base import TRANSPLANT_IMPOSSIBLE
from transplants.core.solution.transplant import Transplant


def _create_transplant_indicators(solver: Solver, donor_to_recipient_scores: np.ndarray) -> np.ndarray:
    donor_to_recipient_transplant_performed = np.zeros_like(donor_to_recipient_scores, dtype="object")
    donor_count, recipient_count = donor_to_recipient_scores.shape
    for i in range(donor_count):
        for j in range(recipient_count):
            if donor_to_recipient_scores[i, j] != TRANSPLANT_IMPOSSIBLE:
                donor_to_recipient_transplant_performed[i, j] = solver.BoolVar(f"{i} -> {j}")

    donor_to_recipient_scores[donor_to_recipient_scores == TRANSPLANT_IMPOSSIBLE] = 1
    return donor_to_recipient_transplant_performed


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


def solution_to_str(solution: np.ndarray, left_padding: int = 3,
                    j_to_related_i: Optional[Dict[int, List[int]]] = None) -> str:
    solution_repr = ""
    header = "  ".join([str(i % 10) for i in range(len(solution[0]))])
    solution_repr += f"{' ' * (left_padding + 2)}{header}\n"
    solution_repr += f"{' ' * (left_padding)}{'-' * 3 * len(solution[0])}\n"
    for i, row in enumerate(solution):
        row_repr = f"{i}{' ' * (left_padding - len(str(i)))}| "
        for j, item in enumerate(row):
            if item == 0:
                color = Fore.WHITE if j % 2 == 0 else Fore.LIGHTBLACK_EX
                if j_to_related_i is not None:
                    related_is = j_to_related_i[j]
                    if i in related_is:
                        color = Fore.CYAN
                addition = f"{color}0{Fore.RESET}"
            elif item == 1:
                addition = f"{Fore.RED}1{Fore.RESET}"
            else:
                raise Exception(f"Unexpected value of solution ({item})")
            row_repr += addition + "  "

        solution_repr += f"{row_repr}\n"
    return solution_repr


def main():
    scorer = HLABloodTypeAdditiveScorer()
    donors, recipients = load_donors_recipients(data_path="../../../test/test_patient_pool.json")

    i_to_donor = dict(enumerate(donors))
    donor_to_i = {value: key for key, value in i_to_donor.items()}

    j_to_recipient = dict(enumerate(recipients))

    j_to_related_i = {j: [donor_to_i[donor] for donor in recipient.related_donors]
                      for j, recipient in j_to_recipient.items()}

    W = np.array(
        [[scorer.score_transplant(Transplant(donor=donor, recipient=recipient)) for recipient in recipients]
         for donor in donors]
    )

    solver = Solver.CreateSolver("GLOP")
    X = _create_transplant_indicators(solver=solver, donor_to_recipient_scores=W)

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
        objective_value = solver.Objective().Value()
        solution = _get_solution_value(X)
        solution = solution.astype("int64")

        print(f"[INFO] Solved. Objective value: {objective_value}")
        print(f"[INFO] Solution is:")
        print(solution_to_str(solution, j_to_related_i=j_to_related_i))
    else:
        print("[ERROR] No solution found")

    print(f"{solver.wall_time()} ms | {solver.iterations()} iterations")


if __name__ == '__main__':
    main()
