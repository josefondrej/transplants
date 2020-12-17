from typing import List

from transplants.core.solution.chain import Chain
from transplants.core.solution.transplant import Transplant


class Cycle(Chain):
    """Chain of transplants ending with the same pair it started with"""

    def __init__(self, transplants: List[Transplant]):
        super().__init__(transplants=transplants, is_cycle=True)
