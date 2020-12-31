from typing import Dict

from transplants.core.solution.chain import Chain
from transplants.core.solution.serialize_to_dict.transplant import to_dict as transplant_to_dict


def to_dict(chain: Chain) -> Dict:
    dictionary = {
        "transplants": [transplant_to_dict(transplant) for transplant in chain.transplants],
        "is_cycle": chain.is_cycle,
        "score": chain.score
    }
    return dictionary
