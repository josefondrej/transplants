import json
from unittest import TestCase

from transplants.problem.patient.patient import Patient
from transplants.utils.paths import get_abs_path


class TestPatient(TestCase):
    def test_de_serialization_all(self):
        """Test if the deserialization and back serialization even finishes"""
        patients_data_path = get_abs_path("tests/test_utils/patient_pool_example.json")

        with open(patients_data_path, "r") as patients_data_file:
            serialized_patients = json.load(patients_data_file)

        deserialized_patients = [Patient.from_dict(serialized_patient)
                                 for serialized_patient in serialized_patients]

        serialized_patients_2 = [patient_model.to_dict()
                                 for patient_model in deserialized_patients]

        self.maxDiff = None
        # for patient, patient_2 in zip(serialized_patients, serialized_patients_2):
        #     self.assertDictContainsSubset(patient, patient_2)
        # TODO: Write proper test here
