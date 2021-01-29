from marshmallow import Schema, fields, post_load
from marshmallow.validate import OneOf

from transplants.problem.patient.medical_data.antigen_antibody_system.utils import anti
from transplants.problem.patient.medical_data.hla_system.antigen_definitions import all_antigens
from transplants.problem.patient.medical_data.hla_system.hla_system import HLASystem as HLASystemModel

_code_to_antigen = {str(antigen): antigen for antigen in all_antigens}

_antigen_code_validator = OneOf(
    [str(antigen) for antigen in all_antigens])  # TODO: Add to antigens and antibodies once there are all the codes


class HLASystemSchema(Schema):
    antigens = fields.List(fields.Str())
    antibodies = fields.Dict(
        keys=fields.Str(),
        values=fields.Float(allow_none=True),
        attribute="_antibody_to_concentration"
    )

    @post_load
    def make_hla_system(self, data, **kwargs) -> HLASystemModel:
        antigens = [_code_to_antigen[code] for code in data["antigens"] if
                    code in _code_to_antigen]  # TODO: Remove after adding validation
        antibodies = {anti(_code_to_antigen[code]): concentration
                      for code, concentration in data["_antibody_to_concentration"].items()
                      if code in _code_to_antigen}
        hla_system_model = HLASystemModel(antigens=set(antigens), antibodies=antibodies)
        return hla_system_model


if __name__ == '__main__':
    from transplants.problem.patient.medical_data import A26, A9, A3, A24, DR7

    # Schema
    schema = HLASystemSchema()

    # Model
    test_hla_system = HLASystemModel(
        antigens={A26, A3, A9},
        antibodies={anti(A24), anti(DR7)}
    )

    # Serialize
    serialized_hla_system = schema.dump(test_hla_system)
    print(serialized_hla_system)

    # Deserialize
    deserialized_hla_system = schema.load(serialized_hla_system)
    print(deserialized_hla_system)
