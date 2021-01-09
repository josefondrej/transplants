from typing import List

from transplants.patient.patient import Patient
from transplants.solution.transplant import Transplant


def get_default_forbidden_transplants(patients: List[Patient]) -> List[Transplant]:
    """List transplants that are forbidden by default -- if recipient is not looking for better match we assume by
    default he can't be transplanted with any of his related donors"""
    default_forbidden_transplants = [
        Transplant(donor=donor, recipient=patient)
        for patient in patients
        if patient.is_recipient and not patient.require_better_than_related_match
        for donor in patient.related_donors
    ]

    return default_forbidden_transplants
