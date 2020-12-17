from typing import Optional

from transplants.core.patient.medical_data.antigen_antibody_system.antigen import Antigen


class HLAAntigen(Antigen):
    def __init__(self, code: str, broad: Optional["HLAAntigen"] = None):
        self._broad = broad
        super().__init__(code=code)

    @property
    def broad(self) -> Optional["HLAAntigen"]:
        return self._broad
