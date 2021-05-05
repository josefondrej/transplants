from abc import ABC
from typing import List, Optional

import numpy as np
from marshmallow import fields

from transplants.serialization.serialization_mixin import add_marshmallow_schema, SerializationMixin, \
    serializable_property
from transplants.solution.scored_mixin import ScoredMixin
from transplants.solution.transplant import Transplant


@add_marshmallow_schema
class Chain(ABC, ScoredMixin, SerializationMixin):
    """General base class for chain of transplants"""

    def __init__(self, transplants: List[Transplant], is_cycle: bool = None):
        self._transplants = transplants
        self._is_cycle = is_cycle

    def __eq__(self, other):
        if not isinstance(other, Chain):
            return False

        if self.is_cycle != other.is_cycle:
            return False

        return set(self.transplants) == set(other.transplants)

    def __hash__(self):
        if not self.is_cycle:
            ordered_transplants = self.transplants
        else:
            # If the chain is a circle then we need to rotate the transplants to the same position
            # in order to be able to compare them
            # Here we choose this starting position as th transplant with the smallest donor index
            # (in lexicographical order)
            first_donor_index = np.argmin([str(transplant.donor_id) for transplant in self.transplants])
            ordered_transplants = self.transplants[first_donor_index:] + self.transplants[:first_donor_index]

        return hash(tuple(hash(transplant) for transplant in ordered_transplants))

    @serializable_property(fields.List(fields.Nested(Transplant.marshmallow_schema)))
    def transplants(self) -> List[Transplant]:
        return self._transplants

    @serializable_property(fields.Bool())
    def is_cycle(self) -> bool:
        return self._is_cycle

    @property
    def length(self) -> int:
        return len(self.transplants)

    def next_transplant(self, transplant: Transplant) -> Optional[Transplant]:
        transplant_index = self.transplants.index(transplant)
        next_transplant_index = transplant_index + 1

        if next_transplant_index >= self.length and not self.is_cycle:
            return None

        return self.transplants[next_transplant_index % self.length]
