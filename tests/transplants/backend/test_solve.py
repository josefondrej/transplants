from tests.test_utils.load_job import load_job
from tests.test_utils.load_problem import load_problem
from tests.test_utils.load_solution import load_solution
from tests.test_utils.load_solver_config import load_solver_config
from tests.test_utils.mock_db import MockDB
from transplants.api.solve import solve
from transplants.api.solve_job import solve_job
from transplants.model.solution import Solution


class TestSolve(MockDB):
    def test_solve(self):
        problem = load_problem()
        solver_config = load_solver_config()
        expected_solution = load_solution()

        solution = solve(problem=problem, solver_config=solver_config)

        print(solution.to_dict())
        print(expected_solution.to_dict())

        self.assertEqual(solution, expected_solution)

    def test_solve_db(self):
        problem = load_problem()
        solver_config = load_solver_config()
        job = load_job()

        problem.save_to_db()
        solver_config.save_to_db()
        job.save_to_db()

        solution_id = solve_job(job.job_id)
        solution = Solution.find_by_id(solution_id)

        expected_solution = load_solution()

        self.assertEqual(solution, expected_solution)
