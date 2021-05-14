from flask_apispec import MethodResource, marshal_with

from transplants.model.solution import Solution


class SolutionResource(MethodResource):
    @marshal_with(Solution.marshmallow_schema)
    def get(self, solution_id: str):
        solution = Solution.find_by_id(solution_id)
        return solution
