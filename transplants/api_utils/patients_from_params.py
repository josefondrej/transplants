import json
from typing import Tuple, List

from transplants.core.patient.donor import Donor
from transplants.core.patient.recipient import Recipient
from transplants.core.patient.serialize_to_dict.patient import from_dict as patient_from_dict, \
    to_dict as patient_to_dict


def patients_from_params(serialized_patients: List) -> Tuple[List[Donor], List[Recipient]]:
    patients = [patient_from_dict(dictionary) for dictionary in serialized_patients]
    donors: List[Donor] = [patient for patient in patients if patient.is_donor]
    recipients: List[Recipient] = [patient for patient in patients if patient.is_recipient]
    identifier_to_donor = {donor.identifier: donor for donor in donors}
    for recipient in recipients:
        recipient._related_donors = [identifier_to_donor[identifier] for identifier in recipient.related_donors]
    return donors, recipients


if __name__ == '__main__':
    with open("./test/test_utils/test_patient_pool.json", "r") as serialized_patients_file:
        test_serialized_patients = json.load(serialized_patients_file)

    test_donors, test_recipients = patients_from_params(test_serialized_patients)
    test_patients = test_donors + test_recipients

    for test_patient in test_patients:
        serialized_patient = patient_to_dict(test_patient)
        print(serialized_patient)
