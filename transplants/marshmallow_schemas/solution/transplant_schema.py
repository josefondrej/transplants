from marshmallow import Schema, fields, post_load, pre_dump

from transplants.solution.transplant import Transplant


class TransplantSchema(Schema):
    donor = fields.String(attribute="donor_id")
    recipient = fields.String(attribute="recipient_id")
    score = fields.Float()

    @pre_dump
    def add_name(self, data, **kwargs):
        data.donor = data.donor_id
        data.recipient = data.recipient_id
        return data

    @post_load
    def make_transplant(self, data, **kwargs) -> Transplant:
        model = Transplant(
            donor_id=data["donor_id"],
            recipient_id=data["recipient_id"]
        )

        model.set_score(data.get("score"))

        return model
