from typing import List

from transplants.core.patient.donor import Donor
from transplants.core.patient.patient import Patient
from transplants.core.patient.patient_data.medical_data import MedicalData


class Recipient(Patient):
    def __init__(self, identifier: str, medical_data: MedicalData, related_donors: List[Donor],
                 related_transplant_is_possible: List[bool] = None):
        """

        Args:
            identifier: Unique identifier for the patient
            medical_data: Patient's medical data
            related_donors: List of relatives / friends that want to donate their kidney to this patient
            related_transplant_is_possible: List that informs us if the transplant with each related donor would be
                possible or not. Some pairs go into the exchange not because they are completely incompatible, but
                because they want to improve the compatibility even more. In this case we can't offer them worse
                match than they already have.
        """
        self._related_donors = related_donors
        self._related_transplant_is_possible = related_transplant_is_possible or [False] * len(related_donors)
        super().__init__(identifier=identifier, medical_data=medical_data)

    @property
    def is_donor(self) -> bool:
        return False

    @property
    def is_recipient(self) -> bool:
        return True

    @property
    def related_donors(self) -> List[Donor]:
        return self._related_donors
