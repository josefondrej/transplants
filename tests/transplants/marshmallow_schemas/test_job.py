from unittest import TestCase

from tests.test_utils.load_job import load_job
from transplants.marshmallow_schemas import JobSchema


class TestJob(TestCase):
    def test_original_equals_deserialized_serialized(self):
        job = load_job()
        job_schema = JobSchema()

        serialized_job = job_schema.dump(job)
        deserialized_job = job_schema.load(serialized_job)

        self.assertEqual(job, deserialized_job)
