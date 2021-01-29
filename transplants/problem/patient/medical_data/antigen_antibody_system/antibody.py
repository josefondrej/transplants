from abc import ABC

from transplants.problem.patient.medical_data.antigen_antibody_system.antigen import Antigen


class Antibody(ABC):
    """Generic class for antibody."""

    def __init__(self, antigen: Antigen):
        self._antigen = antigen

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        else:
            return self.code == other.code

    def __hash__(self):
        return hash(self.code)

    def __str__(self):
        return self.code

    def __repr__(self):
        return self.code

    @property
    def antigen(self) -> Antigen:
        return self._antigen

    @property
    def code(self) -> str:
        return self._antigen.code
