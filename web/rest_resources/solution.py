from web.rest_resources.solution_store_resource import SolutionStoreResource


class Solution(SolutionStoreResource):
    def get(self, token: str):
        # TODO: Support iteration here -- some solutions will be large, you don't want to return them whole
        solution = self.store.get_solution(token)

        if solution is None:
            return {"message": f"Solution {token} does not exist"}, 404

        return solution.to_dict(), 200
