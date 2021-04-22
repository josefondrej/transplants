from unittest import TestCase

from transplants.problem.patient.donor import Donor
from transplants.problem.patient.recipient import Recipient
from transplants.solution.cycle import Cycle
from transplants.solution.matching import Matching
from transplants.solution.sequence import Sequence
from transplants.solution.transplant import Transplant


class TestHashing(TestCase):
    def setUp(self) -> None:
        self.patient_id_a = "aaaa1111"
        self.patient_id_b = "bbbb2222"
        self.patient_id_c = "cccc3333"
        self.patient_id_d = "dddd4444"
        self.patient_id_e = "eeee5555"
        self.patient_id_f = "ffff6666"

        self.patient_a = Donor(identifier=self.patient_id_a, medical_data=None)
        self.patient_b = Recipient(identifier=self.patient_id_b, medical_data=None, related_donor_ids=[])
        self.patient_c = Donor(identifier=self.patient_id_c, medical_data=None)
        self.patient_d = Recipient(identifier=self.patient_id_d, medical_data=None, related_donor_ids=[])
        self.patient_e = Donor(identifier=self.patient_id_e, medical_data=None)
        self.patient_f = Recipient(identifier=self.patient_id_f, medical_data=None, related_donor_ids=[])

        self.transplant_one = Transplant(donor_id=self.patient_id_a, recipient_id=self.patient_id_b)
        self.transplant_two = Transplant(donor_id=self.patient_id_c, recipient_id=self.patient_id_d)
        self.transplant_three = Transplant(donor_id=self.patient_id_e, recipient_id=self.patient_id_f)

    def test_patient_hashing(self):
        self.assertEqual(hash(self.patient_a), hash(self.patient_id_a))

    def test_transplant_hashing(self):
        self.assertEqual(hash(self.transplant_one), hash((hash(self.patient_id_a), hash(self.patient_id_b))))

    def test_sequence_hashing(self):
        chain = Sequence(transplants=[self.transplant_one, self.transplant_two])
        self.assertEqual(
            first=hash(chain),
            second=hash(
                (hash(self.transplant_one), hash(self.transplant_two))
            )
        )

    def test_cycle_hashing(self):
        cycle_one = Cycle(transplants=[self.transplant_one, self.transplant_two, self.transplant_three])
        cycle_one_shifted = Cycle(transplants=[self.transplant_one, self.transplant_two, self.transplant_three])
        cycle_two = Cycle(transplants=[self.transplant_two, self.transplant_one, self.transplant_three])

        self.assertEqual(
            first=hash(cycle_one),
            second=hash(
                (hash(self.transplant_one), hash(self.transplant_two), hash(self.transplant_three))
            )
        )

        self.assertNotEqual(
            first=hash(cycle_one),
            second=hash(
                (hash(self.transplant_one), hash(self.transplant_three), hash(self.transplant_two))
            )
        )
        self.assertEqual(hash(cycle_one), hash(cycle_one_shifted))
        self.assertNotEqual(hash(cycle_one), hash(cycle_two))
        self.assertNotEqual(hash(cycle_one_shifted), hash(cycle_two))

    def test_matching_hashing(self):
        chain_one = Cycle(transplants=[self.transplant_one, self.transplant_two])
        chain_two = Sequence(transplants=[self.transplant_three])
        matching = Matching(chains=[chain_one, chain_two])
        matching_shuffled = Matching(chains=[chain_two, chain_one])

        self.assertEqual(
            first=hash(matching),
            second=hash(tuple(hash(chain) for chain in sorted(matching.chains, key=hash)))
        )
        self.assertEqual(hash(matching), hash(matching_shuffled))
