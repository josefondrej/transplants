from unittest import TestCase

from transplants.problem.patient.medical_data.blood_type_system.blood_type import BloodType


class TestBloodTypeSchema(TestCase):
    def test_de_serialization(self):
        blood_type_serialized = {
            "type": "A",
            "forbidden_types": None
        }

        blood_type_deserialized = BloodType.from_dict(blood_type_serialized)
        blood_type_serialized_again = blood_type_deserialized.to_dict()
        self.assertEqual(blood_type_serialized, blood_type_serialized_again)
