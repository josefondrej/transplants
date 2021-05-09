from marshmallow import fields

from transplants.serialization.serialization_mixin import add_marshmallow_schema, SerializationMixin, \
    serializable_property
from transplants.solution.scored_mixin import ScoredMixin


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
        return hash((hash(self.donor_id), hash(self.recipient_id)))

    @serializable_property(fields.String(), serialize_name="donor")
    def donor_id(self) -> str:
        return self._donor_id

    @serializable_property(fields.String(), serialize_name="recipient")
    def recipient_id(self) -> str:
        return self._recipient_id
