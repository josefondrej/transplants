from typing import List

from transplants.problem.patient.medical_data.medical_data import MedicalData
from transplants.problem.patient.patient import Patient


class Recipient(Patient):
    """Patient that is recipient in the transplant

    Args:
        identifier: Unique identifier for the patient
        medical_data: Patient's medical data
        related_donor_ids: List of relatives / friends that want to donate their kidney to this patient
        require_better_than_related_match: Some pairs enter the program not because the transplant between
            them would be completely impossible but because they want to get a better match than they already have
    """

    def __init__(self, identifier: str, medical_data: MedicalData, related_donor_ids: List[str],
                 require_better_than_related_match: bool = False):
        self._related_donor_ids = related_donor_ids
        self._require_better_than_related_match = require_better_than_related_match
        super().__init__(identifier=identifier, medical_data=medical_data)

    @property
    def is_donor(self) -> bool:
        return False

    @property
    def is_recipient(self) -> bool:
        return True

    @property
    def related_donor_ids(self) -> List[str]:
        return self._related_donor_ids

    @property
    def require_better_than_related_match(self) -> bool:
        return self._require_better_than_related_match