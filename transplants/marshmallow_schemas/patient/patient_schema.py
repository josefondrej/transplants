from marshmallow import Schema, fields, post_load, pre_dump

from transplants.marshmallow_schemas.patient.medical_data.medical_data_schema import MedicalDataSchema
from transplants.problem.patient.donor import Donor
from transplants.problem.patient.patient import Patient
from transplants.problem.patient.patient_type import PatientType
from transplants.problem.patient.recipient import Recipient

_code_to_patient_type = {patient_type.value: patient_type for patient_type in PatientType}


class PatientSchema(Schema):
    identifier = fields.Str()
    patient_type = fields.Str()
    medical_data = fields.Nested(MedicalDataSchema)
    related_donors = fields.List(fields.Str(), attribute="related_donor_ids", required=False)
    require_better_than_related_match = fields.Bool(required=False)
    country = fields.Str(required=False)

    @pre_dump
    def add_patient_type(self, data, **kwargs):
        data.patient_type = str(data.type.value)
        return data

    @post_load
    def make_patient(self, data, **kwargs) -> Patient:
        patient_type = _code_to_patient_type[data["patient_type"]]
        identifier = data["identifier"]
        medical_data = data["medical_data"]

        if patient_type == PatientType.DONOR:
            patient_model = Donor(
                identifier=identifier,
                medical_data=medical_data
            )
        elif patient_type == PatientType.RECIPIENT:
            patient_model = Recipient(
                identifier=identifier,
                medical_data=medical_data,
                related_donor_ids=data["related_donor_ids"],
                require_better_than_related_match=data.get("require_better_than_related_match") or False
            )
        else:
            raise ValueError(f"Incorrect value for patient type {data['patient_type']}")

        return patient_model
