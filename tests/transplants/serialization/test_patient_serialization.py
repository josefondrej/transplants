import json
from unittest import TestCase

from transplants.model.patient import Patient
from transplants.utils.paths import get_abs_path


class TestPatientSerialization(TestCase):
    def test_serialized_equals_serialized_deserialized(self):
        patients_data_path = get_abs_path("tests/test_utils/patient_pool_example.json")

        with open(patients_data_path, "r") as patients_data_file:
            serialized_patients = json.load(patients_data_file)

        deserialized_patients = [Patient.from_dict(serialized_patient)
                                 for serialized_patient in serialized_patients]

        serialized_deserialized_patients = [patient_model.to_dict()
                                            for patient_model in deserialized_patients]

        self.maxDiff = None
        for serialized_patient, serialized_deserialized_patient in zip(serialized_patients,
                                                                       serialized_deserialized_patients):
            self.assertEqual(serialized_patient["identifier"], serialized_deserialized_patient["identifier"])
            self.assertEqual(serialized_patient["patient_type"], serialized_deserialized_patient["patient_type"])
            self.assertEqual(serialized_patient["country"], serialized_deserialized_patient["country"])
            self.assertEqual(serialized_patient["medical_data"]["blood_type"],
                             serialized_deserialized_patient["medical_data"]["blood_type"])

            # Because we load only valid HLA Codes, we have to compare those in the following way
            # which is also reason we compare other fields one by one and not comparing patients as whole
            self.assertTrue(set(serialized_patient["medical_data"]["hla_system"]["antigens"]).issuperset(
                serialized_deserialized_patient["medical_data"]["hla_system"]["antigens"]))

            self.assertTrue(set(serialized_patient["medical_data"]["hla_system"]["antibodies"]).issuperset(
                serialized_deserialized_patient["medical_data"]["hla_system"]["antibodies"]))
