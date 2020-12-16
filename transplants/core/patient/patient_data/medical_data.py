from transplants.core.patient.patient_data.blood_group_system.blood_type import BloodType
from transplants.core.patient.patient_data.hla_system.hla_system import HLASystem


class MedicalData:
    def __init__(self, blood_type: BloodType, hla_system: HLASystem):
        self._blood_type = blood_type
        self._hla_system = hla_system

    @property
    def blood_type(self) -> BloodType:
        return self._blood_type

    @property
    def hla_system(self) -> HLASystem:
        return self._hla_system
