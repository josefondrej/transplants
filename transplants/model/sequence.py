from typing import List

from transplants.model.chain import Chain
from transplants.model.transplant import Transplant


class Sequence(Chain):
    """Chain of transplants ending with a different pair than it started with
    This means that the first donor had to be bridging donor left from previous matching or an altruist"""

    def __init__(self, transplants: List[Transplant]):
        super().__init__(transplants=transplants, is_cycle=False)

    def __eq__(self, other):
        if not isinstance(other, Sequence):
            return False

        return self.transplants == other.transplants

    def __hash__(self):
        return hash(tuple(transplant for transplant in self.transplants))
