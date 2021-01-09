from flask import request

from web.rest_resources.solution_store_resource import SolutionStoreResource
from web.utils.solve_async import solve_async


class SolutionJob(SolutionStoreResource):
    def post(self):
        exchange_parameters = request.get_json()
        token = solve_async(
            exchange_parameters=exchange_parameters,
            solution_store=self.store
        )
        return {"solution_token": token}, 202
