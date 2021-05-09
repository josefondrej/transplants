from typing import Set

from marshmallow import fields

from transplants.problem.patient.medical_data.antigen_antibody_system.antigen_antibody_system import \
    AntigenAntibodySystem
from transplants.problem.patient.medical_data.antigen_antibody_system.utils import anti
from transplants.problem.patient.medical_data.hla_system.antigen_definitions import all_antigens
from transplants.problem.patient.medical_data.hla_system.hla_antibody import HLAAntibody
from transplants.problem.patient.medical_data.hla_system.hla_antigen import HLAAntigen
from transplants.serialization.serialization_mixin import add_marshmallow_schema, SerializationMixin, \
    serializable_property

_code_to_antigen = {str(antigen): antigen for antigen in all_antigens}


@add_marshmallow_schema
class HLASystem(AntigenAntibodySystem, SerializationMixin):
    @serializable_property(fields.List(fields.String()))
    def antigens(self) -> Set[HLAAntigen]:
        return super().antigens

    @serializable_property(fields.Dict(keys=fields.String(), values=fields.Float(allow_none=True)))
    def antibodies(self) -> Set[HLAAntibody]:
        return self._antibodies

    @classmethod
    def _marshmallow_post_load(cls, data):
        antigens = [_code_to_antigen[code] for code in data["antigens"] if code in _code_to_antigen]
        antibodies = {anti(_code_to_antigen[code]): concentration
                      for code, concentration in data["antibodies"].items()
                      if code in _code_to_antigen}
        hla_system = cls(antigens=set(antigens), antibodies=antibodies)
        return hla_system
