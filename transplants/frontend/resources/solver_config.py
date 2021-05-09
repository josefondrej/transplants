from flask_apispec import MethodResource, marshal_with, use_kwargs

from transplants.model.solver_config import SolverConfig as SolverConfigModel


class SolverConfig(MethodResource):
    @marshal_with(SolverConfigModel.marshmallow_schema)
    def get(self, solver_config_id: str):
        solver_config = SolverConfigModel.find_by_id(solver_config_id)
        return solver_config

    @use_kwargs(SolverConfigModel.marshmallow_schema)
    def post(self, solver_config: SolverConfigModel, **kwargs):
        solver_config.save_to_db()
