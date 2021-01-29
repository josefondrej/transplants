from abc import ABC, abstractmethod

from transplants.problem.patient.medical_data.medical_data import MedicalData
from transplants.problem.patient.patient_type import PatientType


class Patient(ABC):
    """Base class representing patient. It should not be instantiated

    Args:
        identifier: Unique identifier for the patient
        medical_data: Patient's medical data
    """

    def __init__(self, identifier: str, medical_data: MedicalData):
        self._identifier = identifier
        self._medical_data = medical_data

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.identifier == other.identifier

    def __hash__(self):
        return hash(self.identifier)

    def __str__(self):
        return self._identifier

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

    @property
    def type(self) -> PatientType:
        patient_type = PatientType.DONOR if self.is_donor else PatientType.RECIPIENT
        return patient_type
