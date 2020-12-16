from typing import Set, Dict, Union

from transplants.core.patient.patient_data.antigen_antibody_system.antibody import Antibody
from transplants.core.patient.patient_data.antigen_antibody_system.antigen import Antigen


class AntigenAntibodySystem:
    def __init__(self, antigens: Set[Antigen], antibodies: Union[Set[Antibody], Dict[Antibody, float]]):
        self._antigens = antigens

        if not isinstance(antibodies, dict):
            self._antibody_to_concentration = {antibody: None for antibody in antibodies}
        else:
            self._antibody_to_concentration = dict(antibodies)

    @property
    def antigens(self) -> Set[Antigen]:
        return self._antigens

    @property
    def antibodies(self) -> Set[Antibody]:
        return set(self._antibody_to_concentration.keys())

    def has_antigens_for(self, antibodies: Set[Antibody]) -> bool:
        return len(set.intersection({antibody.antigen for antibody in antibodies}, self._antigens)) > 0

    def has_antibodies_for(self, antigens: Set[Antigen]) -> bool:
        return len(set.intersection({antibody.antigen for antibody in self.antibodies}, antigens)) > 0
