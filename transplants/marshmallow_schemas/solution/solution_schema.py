from marshmallow import Schema, fields, post_load

from transplants.marshmallow_schemas.solution.matching_schema import MatchingSchema
from transplants.solution.solution import Solution as SolutionModel


class SolutionSchema(Schema):
    solution_id = fields.String()
    problem_id = fields.String()
    matchings = fields.List(fields.Nested(MatchingSchema))

    @post_load
    def make_solution(self, data, **kwargs) -> SolutionModel:
        model = SolutionModel(
            solution_id=data["solution_id"],
            problem_id=data["problem_id"],
            matchings=data["matchings"]
        )

        return model
