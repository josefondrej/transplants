from typing import List

from transplants.solution.matching import Matching


class ProblemSolution:
    def __init__(self, matchings: List[Matching]):
        self._matchings = matchings

    @property
    def matchings(self) -> List[Matching]:
        return self._matchings
