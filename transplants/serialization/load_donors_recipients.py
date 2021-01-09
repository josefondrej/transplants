import json
from typing import Tuple, List

from transplants.patient.donor import Donor
from transplants.patient.recipient import Recipient
from transplants.serialization.patient import from_dict as patient_from_dict, to_dict as patient_to_dict


def load_donors_recipients(serialized_patients: List) -> Tuple[List[Donor], List[Recipient]]:
    patients = [patient_from_dict(dictionary) for dictionary in serialized_patients]
    donors: List[Donor] = [patient for patient in patients if patient.is_donor]
    recipients: List[Recipient] = [patient for patient in patients if patient.is_recipient]
    identifier_to_donor = {donor.identifier: donor for donor in donors}
    for recipient in recipients:
        recipient._related_donors = [identifier_to_donor[identifier] for identifier in recipient.related_donors]
    return donors, recipients


def load_donors_recipients_from_file(file_path: str) -> Tuple[List[Donor], List[Recipient]]:
    with open(file_path, "r") as serialized_patients_file:
        serialized_patients = json.load(serialized_patients_file)

    return load_donors_recipients(serialized_patients)


if __name__ == '__main__':
    test_donors, test_recipients = load_donors_recipients_from_file("./test/test_utils/patient_pool_example.json")
    test_patients = test_donors + test_recipients

    for test_patient in test_patients:
        serialized_patient = patient_to_dict(test_patient)
        print(serialized_patient)
