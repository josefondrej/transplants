from transplants.core.patient.donor import Donor
from transplants.core.patient.recipient import Recipient
from transplants.core.solution.scored_mixin import ScoredMixin


class Transplant(ScoredMixin):
    """Single transplant from donor to recipient"""

    def __init__(self, donor: Donor, recipient: Recipient):
        self._donor = donor
        self._recipient = recipient

    @property
    def donor(self) -> Donor:
        return self._donor

    @property
    def recipient(self) -> Recipient:
        return self._recipient
