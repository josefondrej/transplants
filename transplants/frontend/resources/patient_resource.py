from flask_apispec import MethodResource, use_kwargs, marshal_with

from transplants.model import Patient


class PatientResource(MethodResource):
    @marshal_with(Patient.marshmallow_schema)
    def get(self, patient_id: str):
        patient = Patient.find_by_id(patient_id)
        return patient

    @use_kwargs(Patient.marshmallow_schema)
    def post(self, patient: Patient, **kwargs):
        patient.save_to_db()
