from flask_apispec import MethodResource, use_kwargs, marshal_with

from transplants.marshmallow_schemas import JobSchema
from transplants.solve_api.job import Job as JobModel


class Job(MethodResource):
    @marshal_with(JobSchema)
    def get(self, job_id: str):
        job = JobModel.find_by_id(job_id)
        return job

    @use_kwargs(JobSchema)
    def post(self, job: JobModel, **kwargs):
        job.save_to_db()
