from unittest import TestCase

from test.test_utils.load_solver_config import load_solver_config
from transplants.marshmallow_schemas import SolverConfigSchema


class TestSolverConfig(TestCase):
    def test_original_equals_deserialized_serialized(self):
        solver_config = load_solver_config()
        solver_config_schema = SolverConfigSchema()

        serialized_solver_config = solver_config_schema.dump(solver_config)
        deserialized_solver_config = solver_config_schema.load(serialized_solver_config)

        self.assertEqual(solver_config, deserialized_solver_config)
