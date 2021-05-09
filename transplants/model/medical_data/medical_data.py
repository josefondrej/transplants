from marshmallow import fields

from transplants.model.medical_data.blood_type_system.blood_type import BloodType
from transplants.model.medical_data.hla_system.hla_system import HLASystem
from transplants.serialization.serialization_mixin import SerializationMixin, add_marshmallow_schema, \
    serializable_property


@add_marshmallow_schema
class MedicalData(SerializationMixin):
    """
    Container for all medical data about the patient

    Args:
            blood_type: Blood type
            hla_system: HLA system
    """

    def __init__(self, blood_type: BloodType, hla_system: HLASystem):
        self._blood_type = blood_type
        self._hla_system = hla_system

    @serializable_property(fields.Nested(BloodType.marshmallow_schema))
    def blood_type(self) -> BloodType:
        return self._blood_type

    @serializable_property(fields.Nested(HLASystem.marshmallow_schema))
    def hla_system(self) -> HLASystem:
        return self._hla_system
