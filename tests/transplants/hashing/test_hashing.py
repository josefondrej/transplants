from unittest import TestCase

from transplants.model.cycle import Cycle
from transplants.model.donor import Donor
from transplants.model.matching import Matching
from transplants.model.medical_data.blood_type_system.blood_type import A
from transplants.model.medical_data.hla_system.hla_system import HLASystem
from transplants.model.medical_data.medical_data import MedicalData
from transplants.model.recipient import Recipient
from transplants.model.sequence import Sequence
from transplants.model.transplant import Transplant


class TestHashing(TestCase):
    def setUp(self) -> None:
        self.patient_id_a = "aaaa1111"
        self.patient_id_b = "bbbb2222"
        self.patient_id_c = "cccc3333"
        self.patient_id_d = "dddd4444"
        self.patient_id_e = "eeee5555"
        self.patient_id_f = "ffff6666"

        test_medical_data = MedicalData(blood_type=A, hla_system=HLASystem(antigens=set(), antibodies=set()))

        self.patient_a = Donor(patient_id=self.patient_id_a, medical_data=test_medical_data)
        self.patient_b = Recipient(patient_id=self.patient_id_b, medical_data=test_medical_data, related_donor_ids=[])
        self.patient_c = Donor(patient_id=self.patient_id_c, medical_data=test_medical_data)
        self.patient_d = Recipient(patient_id=self.patient_id_d, medical_data=test_medical_data, related_donor_ids=[])
        self.patient_e = Donor(patient_id=self.patient_id_e, medical_data=test_medical_data)
        self.patient_f = Recipient(patient_id=self.patient_id_f, medical_data=test_medical_data, related_donor_ids=[])

        self.transplant_one = Transplant(donor_id=self.patient_id_a, recipient_id=self.patient_id_b)
        self.transplant_two = Transplant(donor_id=self.patient_id_c, recipient_id=self.patient_id_d)
        self.transplant_three = Transplant(donor_id=self.patient_id_e, recipient_id=self.patient_id_f)

    def test_patient_hashing(self):
        self.assertEqual(hash(self.patient_a), hash(self.patient_id_a))

    def test_transplant_hashing(self):
        self.assertEqual(hash(self.transplant_one), hash((self.patient_id_a, self.patient_id_b)))

    def test_sequence_hashing(self):
        chain = Sequence(transplants=[self.transplant_one, self.transplant_two])
        self.assertEqual(
            first=hash(chain),
            second=hash(
                (self.transplant_one, self.transplant_two)
            )
        )

    def test_cycle_hashing(self):
        cycle_one = Cycle(transplants=[self.transplant_one, self.transplant_two, self.transplant_three])
        cycle_one_shifted = Cycle(transplants=[self.transplant_one, self.transplant_two, self.transplant_three])
        cycle_two = Cycle(transplants=[self.transplant_two, self.transplant_one, self.transplant_three])

        self.assertEqual(
            first=hash(cycle_one),
            second=hash(
                (self.transplant_one, self.transplant_two, self.transplant_three)
            )
        )

        self.assertNotEqual(
            first=hash(cycle_one),
            second=hash(
                (self.transplant_one, self.transplant_three, self.transplant_two)
            )
        )
        self.assertEqual(hash(cycle_one), hash(cycle_one_shifted))
        self.assertNotEqual(hash(cycle_one), hash(cycle_two))
        self.assertNotEqual(hash(cycle_one_shifted), hash(cycle_two))

    def test_matching_hashing(self):
        chain_one = Cycle(transplants=[self.transplant_one, self.transplant_two])
        chain_two = Sequence(transplants=[self.transplant_three])
        matching = Matching(chains={chain_one, chain_two})
        matching_shuffled = Matching(chains={chain_two, chain_one})

        self.assertEqual(
            first=hash(matching),
            second=hash(tuple(chain for chain in sorted(matching.chains, key=hash)))
        )
        self.assertEqual(hash(matching), hash(matching_shuffled))
