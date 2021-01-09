from typing import Dict

from transplants.serialization.chain import to_dict as chain_to_dict, standardize_chain_dict_representation
from transplants.solution.matching import Matching


def to_dict(matching: Matching) -> Dict:
    dictionary = {
        "chains": [chain_to_dict(chain) for chain in matching.chains],
        "score": matching.score
    }
    return dictionary


def standardize_matching_dict_representation(matching: Dict):
    """Reorder chains to standard order (in place)

    List of chains is in standard order if the chains are in standard order (see `standardize_chain`) and the
    first donors of each chain are sorted lexicographically
    """
    for chain in matching["chains"]:
        standardize_chain_dict_representation(chain)

    matching["chains"] = sorted(matching["chains"], key=lambda chain_: chain_["transplants"][0]["donor"])
