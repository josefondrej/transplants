from flask_apispec import MethodResource

from transplants.model.job import Job


class JobsResource(MethodResource):
    def get(self):
        job_collection = Job.get_collection()
        all_jobs = job_collection.find()
        return {"job_ids": [job["job_id"] for job in all_jobs]}
