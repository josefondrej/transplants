from typing import Set

from marshmallow import fields

from transplants.model.chain import Chain
from transplants.model.scored_mixin import ScoredMixin
from transplants.serialization.serialization_mixin import SerializationMixin, add_marshmallow_schema, \
    serializable_property


@add_marshmallow_schema
class Matching(ScoredMixin, SerializationMixin):
    """Set of several transplant chains which can be either cycles or sequences"""

    def __init__(self, chains: Set[Chain]):
        self._chains = chains

    def __eq__(self, other):
        if not isinstance(other, Matching):
            return False

        return set(self.chains) == set(other.chains)

    def __hash__(self):
        ordered_chains = sorted(self.chains, key=hash)
        return hash(tuple(chain for chain in ordered_chains))

    @serializable_property(fields.List(fields.Nested(Chain.marshmallow_schema)))
    def chains(self) -> Set[Chain]:
        return self._chains
