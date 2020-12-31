from typing import Dict

from transplants.core.solution.matching import Matching
from transplants.core.solution.serialize_to_dict.chain import to_dict as chain_to_dict


def to_dict(matching: Matching) -> Dict:
    dictionary = {
        "chains": [chain_to_dict(chain) for chain in matching.chains],
        "score": matching.score
    }
    return dictionary
