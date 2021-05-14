from flask_apispec import MethodResource, use_kwargs, marshal_with

from transplants.model.job import Job


class JobResource(MethodResource):
    @marshal_with(Job.marshmallow_schema)
    def get(self, job_id: str):
        job = Job.find_by_id(job_id)
        return job

    @use_kwargs(Job.marshmallow_schema)
    def post(self, job: Job, **kwargs):
        job.save_to_db()
