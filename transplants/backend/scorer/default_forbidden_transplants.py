from typing import List, Tuple, Dict

from transplants.model.patient import Patient
from transplants.model.patient_type import PatientType


def get_default_forbidden_transplants(patients: List[Patient]) -> List[Tuple[str, str]]:
    """List transplants represented by Tuple[donor.id, recipient.id] that are forbidden by default
    -- if recipient is not looking for better match we assume by
    default he can't be transplanted with any of his related donors"""
    default_forbidden_transplants = [
        (donor_id, patient.identifier)
        for patient in patients
        if patient.is_recipient and not patient.require_better_than_related_match
        for donor_id in patient.related_donor_ids
    ]

    return default_forbidden_transplants


def get_default_forbidden_transplants_from_serialized(serialized_patients: List[Dict]) -> List[Tuple[str, str]]:
    default_forbidden_transplants = [
        (donor_id, patient["identifier"])
        for patient in serialized_patients
        if patient["patient_type"] == PatientType.RECIPIENT.value and not (patient.get(
            "require_better_than_related_match") is True)
        for donor_id in patient["related_donors"]
    ]

    return default_forbidden_transplants
