from typing import List

from transplants.solution.chain import Chain
from transplants.solution.transplant import Transplant


class Sequence(Chain):
    """Chain of transplants ending with a different pair than it started with
    This means that the first donor had to be bridging donor left from previous matching or an altruist"""

    def __init__(self, transplants: List[Transplant]):
        super().__init__(transplants=transplants, is_cycle=False)
