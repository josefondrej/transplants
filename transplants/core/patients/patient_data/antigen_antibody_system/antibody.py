from dataclasses import dataclass

from transplants.core.patients.patient_data.antigen_antibody_system.antigen import Antigen


@dataclass(frozen=True)
class Antibody:
    """Generic class for antibody."""
    antigen: Antigen
    mmol_per_dm_3: float = None

    def __str__(self):
        return f"anti{str(self.antigen)}"
