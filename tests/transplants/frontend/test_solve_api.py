import json
import time

import requests

from tests.test_utils.load_job import load_job_serialized
from tests.test_utils.load_problem import load_problem_serialized
from tests.test_utils.load_solution import load_solution_serialized
from tests.test_utils.load_solver_config import load_solver_config_serialized
from tests.test_utils.mock_server import MockServer
from transplants.model.job import Job
from transplants.model.problem import Problem
from transplants.model.solution import Solution
from transplants.model.solver_config import SolverConfig

_SOLUTION_CALCULATION_TIMEOUT = 3  # seconds


class TestSolveAPI(MockServer):
    def post_get_problem(self):
        serialized_problem = load_problem_serialized()
        problem_id = serialized_problem[Problem.db_id_name]
        json_serialized_problem = json.dumps(serialized_problem)

        problem_url = f"{self.problem_url}{problem_id}"

        response = requests.request(
            "POST",
            url=problem_url,
            headers=self.post_headers,
            data=json_serialized_problem
        )

        self.assertEqual(response.status_code, 200)

        response = requests.request("GET", url=problem_url, headers=self.get_headers)
        self.assertEqual(response.status_code, 200)

        api_retrieved_serialized_problem = json.loads(response.text)

        print(api_retrieved_serialized_problem)

        self.assertEqual(serialized_problem[Problem.db_id_name], api_retrieved_serialized_problem[Problem.db_id_name])

        # TODO: Figure out why the following does not work:
        # self.assertEqual(serialized_problem, api_retrieved_problem_serialized)

    def post_get_solver_config(self):
        serialized_solver_config = load_solver_config_serialized()
        solver_config_id = serialized_solver_config[SolverConfig.db_id_name]
        json_serialized_solver_config = json.dumps(serialized_solver_config)

        solver_config_url = f"{self.solver_config_url}{solver_config_id}"

        response = requests.request(
            "POST",
            url=solver_config_url,
            headers=self.post_headers,
            data=json_serialized_solver_config
        )
        self.assertEqual(response.status_code, 200)

        response = requests.request("GET", solver_config_url, headers=self.get_headers)
        self.assertEqual(response.status_code, 200)

        api_retrieved_serialized_solver_config = json.loads(response.text)

        print(api_retrieved_serialized_solver_config)

        self.assertDictEqual(serialized_solver_config, api_retrieved_serialized_solver_config)

    def post_get_job(self):
        serialized_job = load_job_serialized()
        job_id = serialized_job[Job.db_id_name]
        json_serialized_job = json.dumps(serialized_job)

        job_url = f"{self.job_url}{job_id}"

        response = requests.request(
            "POST",
            url=job_url,
            headers=self.post_headers,
            data=json_serialized_job
        )
        self.assertEqual(response.status_code, 200)

        response = requests.request("GET", job_url, headers=self.get_headers)
        self.assertEqual(response.status_code, 200)

        api_retrieved_serialized_job = json.loads(response.text)
        api_retrieved_serialized_job = {key: value for key, value in api_retrieved_serialized_job.items() if
                                        key in serialized_job.keys()}

        print(api_retrieved_serialized_job)

        self.assertDictEqual(serialized_job, api_retrieved_serialized_job)

        response = requests.request("GET", self.jobs_url, headers=self.get_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.text), {"job_ids": [job_id]})

    def get_solution(self):
        time.sleep(_SOLUTION_CALCULATION_TIMEOUT)  # Give solver daemon some time to calculate the solution
        serialized_job = load_job_serialized()
        serialized_solution = load_solution_serialized()
        problem_id = serialized_job[Problem.db_id_name]
        solver_config_id = serialized_job[SolverConfig.db_id_name]
        response = requests.request("GET", f"{self.solution_url}{problem_id}_{solver_config_id}",
                                    headers=self.get_headers)
        self.assertEqual(response.status_code, 200)
        api_retrieved_solution = json.loads(response.text)

        print(api_retrieved_solution)

        # We can't compare the dicts because the order of the chains in the matchings would cause problems
        self.assertEqual(Solution.from_dict(api_retrieved_solution),
                         Solution.from_dict(serialized_solution))

    def test_solution_api(self):
        print("Testing POST / GET problem")
        self.post_get_problem()

        print("Testing POST / GET solver config")
        self.post_get_solver_config()

        print("Testing POST / GET job")
        self.post_get_job()

        print("Testing POST / GET solution")
        self.get_solution()
