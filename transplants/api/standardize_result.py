from typing import Dict

import numpy as np


def standardize_chain(chain: Dict):
    """Reorder transplants to standard order if the chain is cycle (in place)

    Cycle is in standard order if the first donor is the lowest one of all donors in lexicographical order
    """
    is_cycle = chain["is_cycle"]
    if is_cycle:
        transplants = chain["transplants"]
        first_donor_index = np.argmin([transplant["donor"] for transplant in transplants])
        chain["transplants"] = transplants[first_donor_index:] + transplants[:first_donor_index]


def standardize_matching(matching: Dict):
    """Reorder chains to standard order (in place)

    List of chains is in standard order if the chains are in standard order (see `standardize_chain`) and the
    first donors of each chain are sorted lexicographically
    """
    for chain in matching["chains"]:
        standardize_chain(chain)

    matching["chains"] = sorted(matching["chains"], key=lambda chain: chain["transplants"][0]["donor"])
