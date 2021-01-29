from marshmallow import Schema, fields, post_load, pre_dump
from marshmallow.validate import OneOf

from transplants.problem.patient.medical_data.blood_type_system.blod_type_definitions import A, B, all_types
from transplants.problem.patient.medical_data.blood_type_system.blood_type import BloodType

_code_to_blood_type = {str(blood_type): blood_type for blood_type in all_types}

_blood_type_code_validator = OneOf([str(blood_type) for blood_type in all_types])


class BloodTypeSchema(Schema):
    type = fields.String(validate=_blood_type_code_validator)
    forbidden_types = fields.List(
        fields.Str(validate=_blood_type_code_validator),
        attribute="forbidden_blood_types",
        allow_none=True
    )

    @pre_dump
    def add_type(self, data, **kwargs):
        data.type = str(data)
        return data

    @post_load
    def make_blood_type(self, data, **kwargs) -> BloodType:
        code = data["type"]
        forbidden_codes = data["forbidden_blood_types"] or list()
        model = _code_to_blood_type[code]
        model._forbidden_blood_types = [_code_to_blood_type[code] for code in forbidden_codes]
        return model


if __name__ == '__main__':
    # Schema
    blood_type_schema = BloodTypeSchema()

    # Model
    blood_type_model = A
    blood_type_model._forbidden_blood_types = [B]

    # Serialize
    serialized_blood_type = blood_type_schema.dump(blood_type_model)
    print(serialized_blood_type)

    # Deserialize
    deserialized_blood_type = blood_type_schema.load(serialized_blood_type)
    print(deserialized_blood_type)
