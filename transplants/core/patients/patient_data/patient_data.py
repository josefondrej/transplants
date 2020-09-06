from typing import List

from transplants.core.patients.patient_data.hla_antibody import Antibody
from transplants.core.patients.patient_data.hla_antigen import Antigen
from transplants.core.patients.patient_data.blood_group import BloodGroup


class PatientData:
    def __init__(self, blood_group: BloodGroup, acceptable_blood_groups: List[BloodGroup],
                 antigens: List[Antigen] = None, antibodies: List[Antibody] = None):
        self._blood_group = blood_group
        self._acceptable_blood_groups = acceptable_blood_groups
        self._antigens = antigens
        self._antibodies = antibodies
