from typing import List

import numpy as np

from transplants.solution.chain import Chain
from transplants.solution.transplant import Transplant


class Cycle(Chain):
    """Chain of transplants ending with the same pair it started with"""

    def __init__(self, transplants: List[Transplant]):
        super().__init__(transplants=transplants, is_cycle=True)

    def __eq__(self, other):
        if not isinstance(other, Cycle):
            return False

        return set(self.transplants) == set(other.transplants)

    def __hash__(self):
        # We need to rotate the transplants to the same position in order to be able to compare them
        # Here we choose this starting position as th transplant with the smallest donor index
        # (in lexicographical order)
        first_donor_index = np.argmin([str(transplant.donor_id) for transplant in self.transplants])
        ordered_transplants = self.transplants[first_donor_index:] + self.transplants[:first_donor_index]

        return hash(tuple(transplant for transplant in ordered_transplants))
