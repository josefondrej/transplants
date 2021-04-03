from flask_apispec import MethodResource, marshal_with, use_kwargs

from transplants.marshmallow_schemas import SolverConfigSchema
from transplants.solver.solver_config import SolverConfig as SolverConfigModel


class SolverConfig(MethodResource):
    @marshal_with(SolverConfigSchema)
    def get(self, solver_config_id: str):
        solver_config = SolverConfigModel.find_by_id(solver_config_id)
        return solver_config

    @use_kwargs(SolverConfigSchema)
    def post(self, solver_config: SolverConfigModel, **kwargs):
        solver_config.save_to_db()
