from web.rest_resources.solution_store_resource import SolutionStoreResource


class SolutionList(SolutionStoreResource):
    def get(self):
        solutions = self.store.get_all_solutions()
        return {"solutions": [solution.to_dict() for solution in solutions]}, 200
