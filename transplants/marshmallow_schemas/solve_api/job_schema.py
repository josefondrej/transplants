from marshmallow import Schema, fields, post_load

from transplants.solve_api.job import Job


class JobSchema(Schema):
    job_id = fields.Str()
    problem_id = fields.Str()
    solver_config_id = fields.Str()
    solution_id = fields.Str(allow_none=True, required=False)
    submission_timestamp = fields.DateTime(allow_none=True, required=False)
    solution_start_timestamp = fields.DateTime(allow_none=True, required=False)
    solution_end_timestamp = fields.DateTime(allow_none=True, required=False)

    @post_load
    def make_job(self, data, **kwargs) -> Job:
        model = Job(**data)
        return model
