from typing import List

from transplants.core.patient.donor import Donor
from transplants.core.patient.medical_data.medical_data import MedicalData
from transplants.core.patient.patient import Patient


class Recipient(Patient):
    def __init__(self, identifier: str, medical_data: MedicalData, related_donors: List[Donor],
                 require_better_than_related_match: bool = False):
        """
        Patient that is recipient in the transplant
        Args:
            identifier: Unique identifier for the patient
            medical_data: Patient's medical data
            related_donors: List of relatives / friends that want to donate their kidney to this patient
            require_better_than_related_match: Some pairs enter the program not because the transplant between
                them would be completely impossible but because they want to get a better match than they already have
        """
        self._related_donors = related_donors
        self._require_better_than_related_match = require_better_than_related_match
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

    @property
    def require_better_than_related_match(self) -> bool:
        return self._require_better_than_related_match
