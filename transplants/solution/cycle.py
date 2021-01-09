from typing import List

from transplants.solution.chain import Chain
from transplants.solution.transplant import Transplant


class Cycle(Chain):
    """Chain of transplants ending with the same pair it started with"""

    def __init__(self, transplants: List[Transplant]):
        super().__init__(transplants=transplants, is_cycle=True)
