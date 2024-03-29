from typing import List

from marshmallow import fields

from transplants.database.database_mixin import DatabaseMixin
from transplants.model.donor import Donor
from transplants.model.patient import Patient
from transplants.model.recipient import Recipient
from transplants.serialization.serialization_mixin import SerializationMixin, add_marshmallow_schema, \
    serializable_property


@add_marshmallow_schema
class Problem(SerializationMixin, DatabaseMixin):
    db_id_name = "problem_id"
    db_collection_name = "problem"

    def __init__(self, problem_id: str, patients: List[Patient]):
        self._problem_id = problem_id
        self._patients = patients

        self._patient_id_to_patient = {patient.patient_id: patient for patient in self._patients}

    def __eq__(self, other):
        if not isinstance(other, Problem):
            return False

        return set(self.patients) == set(other.patients)

    def __hash__(self):
        return hash(tuple(sorted(self.patients, key=hash)))

    @serializable_property(fields.String())
    def problem_id(self) -> str:
        return self._problem_id

    @serializable_property(
        fields.List(fields.Nested(Recipient.marshmallow_schema)))
    def patients(self) -> List[Patient]:
        return self._patients

    @property
    def donors(self) -> List[Donor]:
        return [patient for patient in self._patients if patient.is_donor]

    @property
    def recipients(self) -> List[Recipient]:
        return [patient for patient in self._patients if patient.is_recipient]

    def get_patient(self, patient_id: str) -> Patient:
        return self._patient_id_to_patient.get(patient_id)
