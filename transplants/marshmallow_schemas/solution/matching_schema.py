from marshmallow import Schema, fields, post_load

from transplants.marshmallow_schemas.solution.chain_schema import ChainSchema
from transplants.solution.matching import Matching as MatchingModel


class MatchingSchema(Schema):
    chains = fields.List(fields.Nested(ChainSchema))
    score = fields.Float()

    @post_load
    def make_matching(self, data, **kwargs) -> MatchingModel:
        model = MatchingModel(
            chains=data["chains"]
        )

        model.set_score(data.get("score"))

        return model
