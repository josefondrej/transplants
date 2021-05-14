from flask_apispec import MethodResource, marshal_with, use_kwargs

from transplants.model.solver_config import SolverConfig


class SolverConfigResource(MethodResource):
    @marshal_with(SolverConfig.marshmallow_schema)
    def get(self, solver_config_id: str):
        solver_config = SolverConfig.find_by_id(solver_config_id)
        return solver_config

    @use_kwargs(SolverConfig.marshmallow_schema)
    def post(self, solver_config: SolverConfig, **kwargs):
        solver_config.save_to_db()
