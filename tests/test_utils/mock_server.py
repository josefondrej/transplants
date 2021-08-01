import time
from multiprocessing import Process

from tests.test_utils.mock_db import MockDB, mock_kidney_exchange_database
from transplants.frontend.solve_api import start_app


class MockServer(MockDB):
    def setUp(self) -> None:
        super().setUp()

        self.host, self.port = "localhost", 5000
        self.app_start_timeout = 2  # seconds

        self.solve_api = Process(target=start_app,
                                 kwargs=dict(database=mock_kidney_exchange_database,
                                             host=self.host,
                                             port=self.port,
                                             debug=False)
                                 )
        self.solve_api.start()
        time.sleep(self.app_start_timeout)

        self.url_prefix = f"http://{self.host}:{self.port}/"
        self.problem_url = f"{self.url_prefix}problem/"
        self.solver_config_url = f"{self.url_prefix}solver_config/"
        self.solution_url = f"{self.url_prefix}solution/"
        self.job_url = f"{self.url_prefix}job/"
        self.jobs_url = f"{self.url_prefix}jobs/"
        self.patient_url = f"{self.url_prefix}patient/"
        self.shutdown_url = f"{self.url_prefix}shutdown/"

        self.post_headers = {
            'Content-Type': 'application/json'
        }

        self.get_headers = {
            'Accept': 'application/json'
        }

    def tearDown(self) -> None:
        super().tearDown()
        self.solve_api.terminate()
