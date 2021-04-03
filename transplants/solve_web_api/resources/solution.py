from flask_apispec import MethodResource, marshal_with

from transplants.marshmallow_schemas import SolutionSchema
from transplants.solution.solution import Solution as SolutionModel


class Solution(MethodResource):
    @marshal_with(SolutionSchema)
    def get(self, solution_id: str):
        solution = SolutionModel.find_by_id(solution_id)
        return solution
