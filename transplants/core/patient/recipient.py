from typing import List

from transplants.core.patient.donor import Donor
from transplants.core.patient.patient import Patient
from transplants.core.patient.patient_data.medical_data import MedicalData


class Recipient(Patient):
    def __init__(self, identifier: str, medical_data: MedicalData, related_donors: List[Donor]):
        self._related_donors = related_donors
        super().__init__(identifier=identifier, medical_data=medical_data)
