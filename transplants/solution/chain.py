from abc import ABC
from typing import List, Optional, Dict

from marshmallow import fields

from transplants.serialization.serialization_mixin import add_marshmallow_schema, SerializationMixin, \
    serializable_property
from transplants.solution.scored_mixin import ScoredMixin
from transplants.solution.transplant import Transplant


@add_marshmallow_schema
class Chain(ABC, ScoredMixin, SerializationMixin):
    """General base class for chain of transplants"""
    is_cycle_to_constructor = dict()

    def __init__(self, transplants: List[Transplant], is_cycle: bool = None):
        self._transplants = transplants
        self._is_cycle = is_cycle

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

    @classmethod
    def _marshmallow_post_load(cls, data: Dict):
        data = dict(data)
        score = data.pop("score")
        is_cycle = data.pop("is_cycle")
        constructor = Chain.is_cycle_to_constructor[is_cycle]
        model = constructor(**data)
        model.set_score(score)
        return model
