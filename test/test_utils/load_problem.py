import json

from transplants.marshmallow_schemas.patient.patient_schema import PatientSchema
from transplants.problem.problem import Problem
from transplants.utils.paths import get_abs_path


def load_problem() -> Problem:
    patients_data_path = get_abs_path("test/test_utils/patient_pool_example.json")

    with open(patients_data_path, "r") as patients_data_file:
        serialized_patients = json.load(patients_data_file)

    patient_schema = PatientSchema()
    patients = [patient_schema.load(patient) for patient in serialized_patients]

    problem = Problem(problem_id="test_problem", patients=patients)
    return problem
