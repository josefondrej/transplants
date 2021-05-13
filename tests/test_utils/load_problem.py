import json
from typing import Dict

from tests.test_utils.default_ids import PROBLEM_ID
from transplants.model.problem import Problem
from transplants.utils.paths import get_abs_path


def load_problem_serialized(problem_id: str = PROBLEM_ID) -> Dict:
    patients_data_path = get_abs_path("tests/test_utils/patient_pool_example.json")

    with open(patients_data_path, "r") as patients_data_file:
        serialized_patients = json.load(patients_data_file)

    problem_serialized = {"problem_id": problem_id, "patients": serialized_patients}
    return problem_serialized


def load_problem(problem_id: str = PROBLEM_ID) -> Problem:
    problem_serialized = load_problem_serialized(problem_id=problem_id)
    problem = Problem.from_dict(problem_serialized)
    return problem
