from typing import Set, Optional

from transplants.core.patient.medical_data.blood_group_system.blood_type import BloodType
from transplants.core.patient.medical_data.hla_system.hla_system import HLASystem


class MedicalData:
    """
    Container for all medical data about the patient

    Args:
            blood_type: Blood type
            hla_system: HLA system
            forbidden_blood_types: Blood types of donors from which the patient can't receive transplant
                even if we allow transplant across blood group
    """

    def __init__(self, blood_type: BloodType, hla_system: HLASystem,
                 forbidden_blood_types: Optional[Set[BloodType]] = None):
        self._blood_type = blood_type
        self._hla_system = hla_system
        self._forbidden_blood_types = forbidden_blood_types

    @property
    def blood_type(self) -> BloodType:
        return self._blood_type

    @property
    def hla_system(self) -> HLASystem:
        return self._hla_system

    @property
    def forbidden_blood_types(self) -> Optional[Set[BloodType]]:
        return self._forbidden_blood_types
