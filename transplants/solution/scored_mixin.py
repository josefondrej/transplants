from typing import Optional, Callable, Dict

from marshmallow import fields

from transplants.serialization.serialization_mixin import serializable_property


class ScoredMixin:
    """Mixin class that implements storing of score"""

    def set_score(self, score: float):
        self._score = score

    @serializable_property(fields.Float())
    def score(self) -> Optional[float]:
        if hasattr(self, '_score'):
            return self._score
        else:
            return None

    @classmethod
    def _marshmallow_post_load(cls, dictionary: Dict):
        dictionary = dict(dictionary)
        score = dictionary.pop("score")
        model = cls(**dictionary)
        model.set_score(score)
        return model


def assign_result_to_argument(function: Callable[["ScoredMixin"], float]) -> Callable[["ScoredMixin"], float]:
    """Adds side effect which assigns value returned by `function` to it's `ScoredMixin` argument"""

    def decorated_function(self, scored_mixin: "ScoredMixin", *args, **kwargs) -> float:
        score = function(self, scored_mixin, *args, **kwargs)
        scored_mixin.set_score(score)
        return score

    return decorated_function
