from typing import List, Tuple

from transplants.core.patients.donor import Donor
from transplants.core.patients.recipient import Recipient


class Matching:
    def __init__(self, pairs: List[Tuple[Donor, Recipient]]):
        self._pairs = pairs
