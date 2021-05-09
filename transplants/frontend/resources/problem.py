from flask_apispec import MethodResource, use_kwargs, marshal_with

from transplants.model.problem import Problem as ProblemModel


class Problem(MethodResource):
    @marshal_with(ProblemModel.marshmallow_schema)
    def get(self, problem_id: str):
        problem = ProblemModel.find_by_id(problem_id)
        return problem

    @use_kwargs(ProblemModel.marshmallow_schema)
    def post(self, problem: ProblemModel, **kwargs):
        problem.save_to_db()
