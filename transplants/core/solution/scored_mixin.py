from typing import Optional


class ScoredMixin:
    """Mixin class that implements storing of score"""

    def set_score(self, score: float):
        self._score = score

    @property
    def score(self) -> Optional[float]:
        if hasattr(self, '_score'):
            return self._score
        else:
            return None
