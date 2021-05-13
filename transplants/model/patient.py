from abc import ABC, abstractmethod
from typing import List, Optional

from marshmallow import fields
from marshmallow.validate import OneOf

from transplants.model.medical_data.medical_data import MedicalData
from transplants.model.patient_type import PatientType
from transplants.serialization.serialization_mixin import SerializationMixin, serializable_property, \
    add_marshmallow_schema

_code_to_patient_type = {patient_type.value: patient_type for patient_type in PatientType}
_patient_type_validator = OneOf([patient_type for patient_type in list(_code_to_patient_type.keys())])


@add_marshmallow_schema
class Patient(ABC, SerializationMixin):
    """Base class representing patient. It should not be instantiated

    Args:
        patient_id: Unique identifier for the patient
        medical_data: Patient's medical data
    """
    type_to_constructor = dict()

    def __init__(self, patient_id: str, medical_data: MedicalData, country: Optional[str] = None):
        self._identifier = patient_id
        self._medical_data = medical_data
        self._country = country

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.patient_id == other.patient_id

    def __hash__(self):
        return hash(self.patient_id)

    def __str__(self):
        return self._identifier

    @serializable_property(fields.String(required=False, allow_none=True))
    def country(self):
        return self._country

    @serializable_property(fields.String())
    def patient_id(self) -> str:
        return self._identifier

    @serializable_property(fields.Nested(MedicalData.marshmallow_schema))
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

    @serializable_property(fields.Str(validate=_patient_type_validator))
    def patient_type(self):
        return self.type

    @classmethod
    def _marshmallow_pre_dump(cls, data):
        data.patient_type = str(data.type.value)
        return data

    @serializable_property(fields.List(fields.String(), required=False))
    def related_donor_ids(self) -> List[str]:
        return self._related_donor_ids

    @serializable_property(fields.Bool(required=False))
    def require_better_than_related_match(self) -> bool:
        return self._require_better_than_related_match

    @classmethod
    def _marshmallow_post_load(cls, data):
        data = dict(data)
        patient_type = data.pop("patient_type")
        constructor = Patient.type_to_constructor[patient_type]
        return constructor(**data)
