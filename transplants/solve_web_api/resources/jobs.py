from flask_apispec import MethodResource

from transplants.database.mongo_db import job_collection


class Jobs(MethodResource):
    def get(self):
        all_jobs = job_collection.find()
        return {"job_ids": [job["job_id"] for job in all_jobs]}
