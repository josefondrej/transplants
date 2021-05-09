from transplants.model.patient import Patient
from transplants.serialization.serialization_mixin import add_marshmallow_schema


@add_marshmallow_schema
class Donor(Patient):
    @property
    def is_donor(self) -> bool:
        return True

    @property
    def is_recipient(self) -> bool:
        return False
