from flask_apispec import MethodResource, marshal_with

from transplants.model.solution import Solution as SolutionModel


class Solution(MethodResource):
    @marshal_with(SolutionModel.marshmallow_schema)
    def get(self, solution_id: str):
        solution = SolutionModel.find_by_id(solution_id)
        return solution
