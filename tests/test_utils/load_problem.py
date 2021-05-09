import json

from tests.test_utils.default_ids import PROBLEM_ID
from transplants.model.patient import Patient
from transplants.model.problem import Problem
from transplants.utils.paths import get_abs_path


def load_problem(problem_id: str = PROBLEM_ID) -> Problem:
    patients_data_path = get_abs_path("tests/test_utils/patient_pool_example.json")

    with open(patients_data_path, "r") as patients_data_file:
        serialized_patients = json.load(patients_data_file)

    patients = [Patient.from_dict(patient) for patient in serialized_patients]

    problem = Problem(problem_id=problem_id, patients=patients)
    return problem
