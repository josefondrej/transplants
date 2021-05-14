import json

import requests

from tests.test_utils.load_patient import load_patient_serialized
from tests.test_utils.mock_db import MockDB
from transplants.model import Patient


class TestPatientAPI(MockDB):
    def setUp(self) -> None:
        super().setUp()

        self.host, self.port = "localhost", 5000

        self.patient_url = f"http://{self.host}:{self.port}/patient/"

        self.post_headers = {
            'Content-Type': 'application/json'
        }

        self.get_headers = {
            'Accept': 'application/json'
        }

    def test_post_get_patient(self):
        patient_serialized = load_patient_serialized()
        patient_id = patient_serialized[Patient.db_id_name]
        json_serialized_patient = json.dumps(patient_serialized)

        patient_url = f"{self.patient_url}{patient_id}"

        response = requests.request(
            "POST",
            url=patient_url,
            headers=self.post_headers,
            data=json_serialized_patient
        )

        self.assertEqual(response.status_code, 200)

        response = requests.request("GET", url=patient_url, headers=self.get_headers)
        self.assertEqual(response.status_code, 200)

        api_retrieved_patient = json.loads(response.text)
        self.assertEqual(api_retrieved_patient[Patient.db_id_name], patient_serialized[Patient.db_id_name])
        self.assertDictEqual(api_retrieved_patient, patient_serialized)
