from unittest import TestCase

from tests.test_utils.load_solver_config import load_solver_config
from transplants.solver.solver_config import SolverConfig


class TestSolverConfig(TestCase):
    def test_original_equals_deserialized_serialized(self):
        solver_config = load_solver_config()

        serialized_solver_config = SolverConfig.to_dict(solver_config)
        deserialized_solver_config = SolverConfig.from_dict(serialized_solver_config)

        self.assertEqual(solver_config, deserialized_solver_config)
