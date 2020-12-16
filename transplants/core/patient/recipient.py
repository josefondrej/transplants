from typing import List

from transplants.core.patient.donor import Donor
from transplants.core.patient.patient import Patient
from transplants.core.patient.patient_data.patient_data import PatientData


class Recipient(Patient):
    def __init__(self, identifier: str, patient_data: PatientData, related_donors: List[Donor]):
        self._related_donors = related_donors
        super().__init__(identifier=identifier, patient_data=patient_data)
