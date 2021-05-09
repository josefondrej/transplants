import json
from typing import Tuple, List

from transplants.problem.patient import Patient
from transplants.problem.patient.donor import Donor
from transplants.problem.patient.recipient import Recipient


def load_donors_recipients(serialized_patients: List) -> Tuple[List[Donor], List[Recipient]]:
    patients = [Patient.from_dict(dictionary) for dictionary in serialized_patients]
    donors: List[Donor] = [patient for patient in patients if patient.is_donor]
    recipients: List[Recipient] = [patient for patient in patients if patient.is_recipient]
    return donors, recipients


def load_donors_recipients_from_file(file_path: str) -> Tuple[List[Donor], List[Recipient]]:
    with open(file_path, "r") as serialized_patients_file:
        serialized_patients = json.load(serialized_patients_file)

    return load_donors_recipients(serialized_patients)


if __name__ == '__main__':
    test_donors, test_recipients = load_donors_recipients_from_file("./tests/test_utils/patient_pool_example.json")
    test_patients = test_donors + test_recipients

    for test_patient in test_patients:
        serialized_patient = test_patient.to_dict()
        print(serialized_patient)
