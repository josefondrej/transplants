import logging
from queue import Queue
from threading import Thread

from transplants.api.solve_job import solve_job
from transplants.model.job import Job

_job_ids_queue = Queue()

_logger = logging.getLogger(name="job_processing")


def _update_job_ids_queue_from_database():
    _logger.info("Initializing job ids queue from database")
    job_collection = Job.get_collection()
    new_jobs = job_collection.find(filter={"solution_start_timestamp": None})
    new_job_ids = [job["job_id"] for job in new_jobs]
    for job_id in new_job_ids:
        _job_ids_queue.put(job_id)


def _solve_daemon():
    while True:
        _logger.info("Waiting for new jobs")
        job_id = _job_ids_queue.get(block=True)
        _logger.info(f"Solving job {job_id}")
        solve_job(job_id=job_id)


def _hook_job_save_to_db():
    _logger.info("Hooking Job.save_to_db")
    original_save_to_db = Job.save_to_db

    def hooked_save_to_db(self):
        original_save_to_db(self)
        _job_ids_queue.put(self.job_id)

    Job.save_to_db = hooked_save_to_db


def start_job_processing() -> Thread:
    _update_job_ids_queue_from_database()
    _hook_job_save_to_db()
    thread = Thread(target=_solve_daemon)
    thread.start()
    return thread
