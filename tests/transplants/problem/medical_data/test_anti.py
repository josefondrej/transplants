from unittest import TestCase

from transplants.problem.patient.medical_data.antigen_antibody_system.utils import anti
from transplants.problem.patient.medical_data.blood_type_system.blood_type_antibody import BloodTypeAntibody
from transplants.problem.patient.medical_data.blood_type_system.blood_type_antigen import BloodTypeAntigen
from transplants.problem.patient.medical_data.hla_system.hla_antibody import HLAAntibody
from transplants.problem.patient.medical_data.hla_system.hla_antigen import HLAAntigen


class TestAnti(TestCase):
    def test_anti(self):
        blood_antigen = BloodTypeAntigen("A")
        blood_anitbody = anti(blood_antigen)
        expected_blood_antibody = BloodTypeAntibody(antigen=blood_antigen)
        self.assertEqual(blood_anitbody, expected_blood_antibody)

        hla_antigen = HLAAntigen("A19")
        hla_antibody = anti(hla_antigen)
        expected_hla_antibody = HLAAntibody(antigen=hla_antigen)
        self.assertEqual(hla_antibody, expected_hla_antibody)
