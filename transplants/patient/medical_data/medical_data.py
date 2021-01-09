from transplants.patient.medical_data.blood_type_system.blood_type import BloodType
from transplants.patient.medical_data.hla_system.hla_system import HLASystem


class MedicalData:
    """
    Container for all medical data about the patient

    Args:
            blood_type: Blood type
            hla_system: HLA system
    """

    def __init__(self, blood_type: BloodType, hla_system: HLASystem):
        self._blood_type = blood_type
        self._hla_system = hla_system

    @property
    def blood_type(self) -> BloodType:
        return self._blood_type

    @property
    def hla_system(self) -> HLASystem:
        return self._hla_system
