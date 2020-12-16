from transplants.core.patient.patient_data.medical_data import MedicalData


class Patient:
    def __init__(self, identifier: str, medical_data: MedicalData):
        self._identifier = identifier
        self._medical_data = medical_data

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def medical_data(self) -> MedicalData:
        return self._medical_data
