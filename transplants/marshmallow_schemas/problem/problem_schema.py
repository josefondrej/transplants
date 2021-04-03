from marshmallow import Schema, fields, post_load

from transplants.problem.problem import Problem as ProblemModel
from transplants.marshmallow_schemas.problem.patient.patient_schema import PatientSchema


class ProblemSchema(Schema):
    problem_id = fields.String()
    patients = fields.List(fields.Nested(PatientSchema))

    @post_load
    def make_problem(self, data, **kwargs) -> ProblemModel:
        model = ProblemModel(
            problem_id=data["problem_id"],
            patients=data["patients"]
        )

        return model
