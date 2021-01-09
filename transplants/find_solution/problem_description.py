from typing import List

from transplants.patient.donor import Donor
from transplants.patient.patient import Patient
from transplants.patient.recipient import Recipient
from transplants.scorer.scorer_base import ScorerBase
from transplants.solver.solver_base import SolverBase


class ProblemDescription:
    def __init__(self, patients: List[Patient], scorer: ScorerBase, solver: SolverBase):
        self._patients = patients
        self._scorer = scorer
        self._solver = solver

    @property
    def patients(self) -> List[Patient]:
        return self._patients

    @property
    def scorer(self) -> ScorerBase:
        return self._scorer

    @property
    def solver(self) -> SolverBase:
        return self._solver

    @property
    def donors(self) -> List[Donor]:
        return [patient for patient in self._patients if patient.is_donor]

    @property
    def recipients(self) -> List[Recipient]:
        return [patient for patient in self._patients if patient.is_recipient]
