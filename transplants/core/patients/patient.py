from transplants.core.patients.patient_data.patient_data import PatientData


class Patient:
    def __init__(self, identifier: str, patient_data: PatientData):
        self._identifier = identifier
        self._patient_data = patient_data
