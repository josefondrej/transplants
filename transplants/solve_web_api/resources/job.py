from flask_apispec import MethodResource, use_kwargs, marshal_with

from transplants.solve_api.job import Job as JobModel


class Job(MethodResource):
    @marshal_with(JobModel.marshmallow_schema)
    def get(self, job_id: str):
        job = JobModel.find_by_id(job_id)
        return job

    @use_kwargs(JobModel.marshmallow_schema)
    def post(self, job: JobModel, **kwargs):
        job.save_to_db()
