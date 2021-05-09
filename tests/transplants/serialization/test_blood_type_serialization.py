from unittest import TestCase

from transplants.model.medical_data.blood_type_system.blood_type import BloodType


class TestBloodTypeSerialization(TestCase):
    def test_original_equals_serialized_deserialized(self):
        blood_type_serialized = {
            "type": "A",
            "forbidden_types": None
        }

        blood_type_deserialized = BloodType.from_dict(blood_type_serialized)
        blood_type_serialized_deserialized = blood_type_deserialized.to_dict()

        self.assertEqual(blood_type_serialized, blood_type_serialized_deserialized)
