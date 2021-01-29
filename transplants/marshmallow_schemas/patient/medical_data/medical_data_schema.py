from marshmallow import Schema, post_load, fields

from transplants.problem.patient.medical_data.medical_data import MedicalData
from transplants.marshmallow_schemas.patient.medical_data.blood_type_schema import BloodTypeSchema
from transplants.marshmallow_schemas.patient.medical_data.hla_system_schema import HLASystemSchema


class MedicalDataSchema(Schema):
    blood_type = fields.Nested(BloodTypeSchema)
    hla_system = fields.Nested(HLASystemSchema)

    @post_load
    def make_medical_data(self, data, **kwargs) -> MedicalData:
        medical_data_model = MedicalData(
            blood_type=data["blood_type"],
            hla_system=data["hla_system"]
        )
        return medical_data_model
