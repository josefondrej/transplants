from transplants.solution.scored_mixin import ScoredMixin


class Transplant(ScoredMixin):
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

    @property
    def donor_id(self) -> str:
        return self._donor_id

    @property
    def recipient_id(self) -> str:
        return self._recipient_id
