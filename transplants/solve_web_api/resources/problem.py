from flask_apispec import MethodResource, use_kwargs, marshal_with

from transplants.marshmallow_schemas import ProblemSchema
from transplants.problem.problem import Problem as ProblemModel


class Problem(MethodResource):
    @marshal_with(ProblemSchema)
    def get(self, problem_id: str):
        problem = ProblemModel.find_by_id(problem_id)
        return problem

    @use_kwargs(ProblemSchema)
    def post(self, problem: ProblemModel, **kwargs):
        problem.save_to_db()
