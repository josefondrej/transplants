from typing import List, Optional

from transplants.model.medical_data.medical_data import MedicalData
from transplants.model.patient import Patient
from transplants.serialization.serialization_mixin import add_marshmallow_schema


@add_marshmallow_schema
class Recipient(Patient):
    """Patient that is recipient in the transplant

    Args:
        patient_id: Unique identifier for the patient
        medical_data: Patient's medical data
        related_donor_ids: List of relatives / friends that want to donate their kidney to this patient
        require_better_than_related_match: Some pairs enter the program not because the transplant between
            them would be completely impossible but because they want to get a better match than they already have
    """

    def __init__(self, patient_id: str, medical_data: MedicalData, related_donor_ids: List[str],
                 require_better_than_related_match: bool = False, country: Optional[str] = None):
        self._related_donor_ids = related_donor_ids
        self._require_better_than_related_match = require_better_than_related_match
        super().__init__(patient_id=patient_id, medical_data=medical_data, country=country)

    @property
    def is_donor(self) -> bool:
        return False

    @property
    def is_recipient(self) -> bool:
        return True
