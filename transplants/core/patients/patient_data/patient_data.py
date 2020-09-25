from typing import List

from transplants.core.patients.patient_data.hla_antibody import HLAAntibody
from transplants.core.patients.patient_data.hla_antigen import HLAAntigen
from transplants.core.patients.patient_data.blood_type import BloodType


class PatientData:
    def __init__(self, blood_type: BloodType, acceptable_blood_types: List[BloodType],
                 hla_antigens: List[HLAAntigen] = None, hla_antibodies: List[HLAAntibody] = None):
        self._blood_type = blood_type
        self._acceptable_blood_types = acceptable_blood_types
        self._hla_antigens = hla_antigens
        self._hla_antibodies = hla_antibodies
