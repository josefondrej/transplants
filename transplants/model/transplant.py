from marshmallow import fields

from transplants.model.scored_mixin import ScoredMixin
from transplants.serialization.serialization_mixin import add_marshmallow_schema, SerializationMixin, \
    serializable_property


@add_marshmallow_schema
class Transplant(ScoredMixin, SerializationMixin):
    """Single transplant represented by  (donor, recipient) pair of patients"""

    def __init__(self, donor_id: str, recipient_id: str):
        self._donor_id = donor_id
        self._recipient_id = recipient_id

    def __eq__(self, other):
        if not isinstance(other, Transplant):
            return False

        return (self.donor_id == other.donor_id) and (self.recipient_id == other.recipient_id)

    def __hash__(self):
        return hash((self.donor_id, self.recipient_id))

    @serializable_property(fields.String())
    def donor_id(self) -> str:
        return self._donor_id

    @serializable_property(fields.String())
    def recipient_id(self) -> str:
        return self._recipient_id
