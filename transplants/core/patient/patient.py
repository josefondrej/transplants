from abc import ABC, abstractmethod

from transplants.core.patient.patient_data.medical_data import MedicalData


class Patient(ABC):
    def __init__(self, identifier: str, medical_data: MedicalData):
        """
        Base class representing patient. It should not be instantiated
        Args:
            identifier: Unique identifier for the patient
            medical_data: Patient's medical data
        """
        self._identifier = identifier
        self._medical_data = medical_data

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def medical_data(self) -> MedicalData:
        return self._medical_data

    @property
    @abstractmethod
    def is_donor(self) -> bool:
        pass

    @property
    @abstractmethod
    def is_recipient(self) -> bool:
        pass
