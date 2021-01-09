from typing import Dict

from transplants.patient.donor import Donor
from transplants.patient.patient import Patient
from transplants.patient.patient_type import PatientType
from transplants.patient.recipient import Recipient
from transplants.serialization.medical_data import to_dict as medical_data_to_dict, from_dict as medical_data_from_dict
from transplants.serialization.patient_type import to_str as patient_type_to_str, from_str as patient_type_from_str


def to_dict(patient: Patient) -> Dict:
    dictionary = {
        "identifier": patient.identifier,
        "patient_type": patient_type_to_str(patient.type),
        "medical_data": medical_data_to_dict(patient.medical_data)
    }

    if patient.is_recipient:
        dictionary["related_donors"] = [donor.identifier for donor in patient.related_donors]
        dictionary["require_better_than_related_match"] = patient.require_better_than_related_match

    return dictionary


def from_dict(dictionary: Dict) -> Patient:
    patient = None

    patient_type = patient_type_from_str(dictionary["patient_type"])
    identifier = dictionary["identifier"]
    medical_data = medical_data_from_dict(dictionary["medical_data"])

    if patient_type == PatientType.DONOR:
        patient = Donor(
            identifier=identifier,
            medical_data=medical_data
        )

    if patient_type == PatientType.RECIPIENT:
        patient = Recipient(
            identifier=identifier,
            medical_data=medical_data,
            related_donors=dictionary["related_donors"],
            require_better_than_related_match=dictionary.get("require_better_than_related_match")
        )

    return patient
