from unittest import TestCase

from tests.test_utils.load_job import load_job
from transplants.solve_api.job import Job


class TestJobSerialization(TestCase):
    def test_original_equals_deserialized_serialized(self):
        job = load_job()

        serialized_job = Job.to_dict(job)
        deserialized_job = Job.from_dict(serialized_job)

        self.assertEqual(job, deserialized_job)
