import json
from unittest import TestCase

from transplants.marshmallow_schemas.patient.patient_schema import PatientSchema


class TestPatient(TestCase):
    def test_de_serialization(self):
        """Test if the deserialization and back serialization even finishes"""
        patients_data_path = "./test/test_utils/patient_pool_example.json"

        with open(patients_data_path, "r") as patients_data_file:
            serialized_patients = json.load(patients_data_file)

        patient_schema = PatientSchema()
        deserialized_patients = [patient_schema.load(serialized_patient)
                                 for serialized_patient in serialized_patients]
        serialized_patients_2 = [patient_schema.dump(patient_model) for patient_model in deserialized_patients]
        print(serialized_patients_2)
