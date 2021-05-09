from unittest import TestCase

from transplants.problem.patient.medical_data.hla_system.hla_system import HLASystem


class TestHLASystemSerialization(TestCase):
    def test_serialized_equals_serialized_deserialized(self):
        serialized_hla_system = {
            'antigens': {'A11', 'A26', 'B62', 'B38', 'DR4', 'DR11', 'DR53', 'DR52', 'DQ7', 'DQ8'}, 'antibodies': {}}

        deserialized_hla_system = HLASystem.from_dict(serialized_hla_system)
        serialized_deserialized_hla_system = deserialized_hla_system.to_dict()

        self.maxDiff = None
        self.assertEqual(set(serialized_hla_system["antigens"]), set(serialized_deserialized_hla_system["antigens"]))
        self.assertEqual(set(serialized_hla_system["antibodies"]),
                         set(serialized_deserialized_hla_system["antibodies"]))
