from marshmallow import Schema, fields, post_load

from transplants.solver.solver_config import SolverConfig


class SolverConfigSchema(Schema):
    solver_config_id = fields.String()
    solver_name = fields.String()
    parameters = fields.Dict()

    @post_load
    def make_solver_config(self, data, **kwargs) -> SolverConfig:
        model = SolverConfig(
            solver_config_id=data["solver_config_id"],
            solver_name=data["solver_name"],
            parameters=data["parameters"]
        )

        return model
