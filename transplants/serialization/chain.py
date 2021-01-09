from typing import Dict

import numpy as np

from transplants.serialization.transplant import to_dict as transplant_to_dict
from transplants.solution.chain import Chain


def to_dict(chain: Chain) -> Dict:
    dictionary = {
        "transplants": [transplant_to_dict(transplant) for transplant in chain.transplants],
        "is_cycle": chain.is_cycle,
        "score": chain.score
    }
    return dictionary


def standardize_chain_dict_representation(chain: Dict):
    """Reorder transplants to standard order if the chain is cycle (in place)

    Cycle is in standard order if the first donor is the lowest one of all donors in lexicographical order
    """
    is_cycle = chain["is_cycle"]
    if is_cycle:
        transplants = chain["transplants"]
        first_donor_index = np.argmin([transplant["donor"] for transplant in transplants])
        chain["transplants"] = transplants[first_donor_index:] + transplants[:first_donor_index]
