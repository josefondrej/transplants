from marshmallow import Schema, fields, post_load

from transplants.marshmallow_schemas.solution.transplant_schema import TransplantSchema
from transplants.solution.chain import Chain as ChainModel
from transplants.solution.cycle import Cycle
from transplants.solution.sequence import Sequence


class ChainSchema(Schema):
    transplants = fields.List(fields.Nested(TransplantSchema))
    is_cycle = fields.Bool()
    score = fields.Float()

    @post_load
    def make_chain(self, data, **kwargs) -> ChainModel:
        ChainConstructor = Cycle if data["is_cycle"] else Sequence
        model = ChainConstructor(
            transplants=data["transplants"]
        )

        model.set_score(data.get("score"))

        return model
