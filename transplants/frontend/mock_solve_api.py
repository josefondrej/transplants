from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app=app)


@app.route('/donor_ids/')
def get_donor_ids():
    return ['abcdef', 'aaaaaa', 'bbbbbb']


@app.route('/patient/TEST_PATIENT_ID')
def get_test_patient():
    test_patient = {
        "country": "AUT",
        "medical_data": {
            "blood_type": {
                "forbidden_types": [
                    "A",
                    "AB",
                    "B"
                ],
                "type": "0"
            },
            "hla_system": {
                "antibodies": {
                    "A11": None,
                    "A24": None,
                    "A25": None,
                    "A26": None,
                    "A29": None,
                    "A3": None,
                    "A30": None,
                    "A31": None,
                    "A32": None,
                    "A34": None,
                    "A36": None,
                    "A43": None,
                    "A66": None,
                    "A74": None,
                    "B13": None,
                    "B42": None,
                    "B49": None,
                    "B51": None,
                    "B52": None,
                    "B54": None,
                    "B55": None,
                    "B57": None,
                    "B58": None,
                    "B59": None,
                    "B63": None
                },
                "antigens": [
                    "DR7",
                    "B41",
                    "B15",
                    "B62",
                    "A2",
                    "B63",
                    "A1",
                    "DR11"
                ]
            }
        },
        "patient_id": "test_patient_id",
        "patient_type": "recipient",
        "related_donor_ids": [
            "3ad4cac"
        ],
        "require_better_than_related_match": False
    }

    return test_patient


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
