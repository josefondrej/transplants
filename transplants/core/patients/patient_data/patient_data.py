from transplants.core.patients.patient_data.blood_group_system.blood_type import BloodType
from transplants.core.patients.patient_data.hla_system.hla_system import HLASystem


class PatientData:
    def __init__(self, blood_type: BloodType, hla_system: HLASystem):
        self._blood_type = blood_type
        self._hla_system = hla_system
