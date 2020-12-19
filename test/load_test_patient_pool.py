import json
from typing import List, Tuple

from transplants.core.patient.donor import Donor
from transplants.core.patient.recipient import Recipient
from transplants.core.serdes import patient
from transplants.core.serdes.patient import to_dict as patient_to_dict


def load_donors_recipients(data_path: str = "test_patient_pool.json") -> Tuple[List[Donor], List[Recipient]]:
    with open(data_path, "r") as test_data_file:
        test_data_raw = json.load(test_data_file)

    patients = [patient.from_dict(dictionary) for dictionary in test_data_raw]
    donors = [patient for patient in patients if patient.is_donor]
    recipients = [patient for patient in patients if patient.is_recipient]
    identifier_to_donor = {donor.identifier: donor for donor in donors}
    for recipient in recipients:
        recipient._related_donors = [identifier_to_donor[identifier] for identifier in recipient.related_donors]
    return donors, recipients


if __name__ == '__main__':
    test_donors, test_recipients = load_donors_recipients()
    test_patients = list()
    test_patients.extend(test_donors)
    test_patients.extend(test_recipients)

    for test_patient in test_patients:
        serialized_patient = patient_to_dict(test_patient)
        print(serialized_patient)
