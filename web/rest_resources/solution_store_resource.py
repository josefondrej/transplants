from flask_restful import Resource

from web.utils.solution_store import SolutionStore


class SolutionStoreResource(Resource):
    def __init__(self, solution_store: SolutionStore):
        self._solution_store = solution_store

    @property
    def store(self) -> SolutionStore:
        return self._solution_store
