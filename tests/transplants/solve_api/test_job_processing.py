# TODO: Implement some debug feature in the start_job_processing() function that allows this to run for finite number of jobs
# from unittest import TestCase
#
# from tests.test_utils.load_job import load_job
# from tests.test_utils.load_problem import load_problem
# from tests.test_utils.load_solver_config import load_solver_config
# from transplants.database.mongo_db import kidney_exchange_database, initialize_db
# from transplants.database.purge_db import purge_db
# from transplants.solve_api.job_processing import start_job_processing
#
#
# class TestJobProcessing(TestCase):
#     def test_processing(self):
#         purge_db(kidney_exchange_database)
#         initialize_db(kidney_exchange_database)
#
#         start_job_processing()
#
#         for i in range(5):
#             problem_id, solver_config_id, job_id = f"problem_{i}", f"solver_config_{i}", f"job_{i}"
#             problem = load_problem(problem_id=problem_id)
#             solver_config = load_solver_config(solver_config_id=solver_config_id)
#             job = load_job(job_id=job_id, problem_id=problem_id, solver_config_id=solver_config_id)
#
#             problem.save_to_db()
#             solver_config.save_to_db()
#             job.save_to_db()
#
#
