from typing import List

from transplants.problem.patient.donor import Donor
from transplants.problem.patient.patient import Patient
from transplants.problem.patient.recipient import Recipient


class Problem:
    """Description of the Kidney Exchange Matching problem
    Does not contain any information on how we should find solution or evaluate it's quality
    """

    def __init__(self, problem_id: str, patients: List[Patient]):
        self._problem_id = problem_id
        self._patients = patients

        self._patient_id_to_patient = {patient.identifier: patient for patient in self._patients}

    @property
    def problem_id(self) -> str:
        return self._problem_id

    @property
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