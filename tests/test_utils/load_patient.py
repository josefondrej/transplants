import json
from typing import Dict

from tests.test_utils.default_ids import PATIENT_ID
from transplants.model import Patient
from transplants.utils.paths import get_abs_path


def load_patient_serialized() -> Dict:
    recipient_example_path = get_abs_path("tests/test_utils/recipient_example.json")
    with open(recipient_example_path, "r") as file:
        serialized_recipient = json.load(file)
    serialized_recipient[Patient.db_id_name] = PATIENT_ID
    return serialized_recipient


def load_patient() -> Patient:
    serialized_patient = load_patient_serialized()
    patient = Patient.from_dict(serialized_patient)
    return patient
