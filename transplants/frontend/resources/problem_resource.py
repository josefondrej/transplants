from flask_apispec import MethodResource, use_kwargs, marshal_with

from transplants.model.problem import Problem


class ProblemResource(MethodResource):
    @marshal_with(Problem.marshmallow_schema)
    def get(self, problem_id: str):
        problem = Problem.find_by_id(problem_id)
        return problem

    @use_kwargs(Problem.marshmallow_schema)
    def post(self, problem: Problem, **kwargs):
        problem.save_to_db()
