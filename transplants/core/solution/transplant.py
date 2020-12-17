from transplants.core.patient.donor import Donor
from transplants.core.patient.recipient import Recipient
from transplants.core.solution.scored_mixin import ScoredMixin


class Transplant(ScoredMixin):
    """Single transplant from donor to recipient"""

    def __init__(self, donor: Donor, recipient: Recipient):
        self._donor = donor
        self._recipient = recipient

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.donor == other.donor) and (self.recipient == other.recipient)

    def __hash__(self):
        return hash((hash(self.donor), hash(self.recipient)))

    @property
    def donor(self) -> Donor:
        return self._donor

    @property
    def recipient(self) -> Recipient:
        return self._recipient
