from typing import Dict

from transplants.solution.transplant import Transplant


def to_dict(transplant: Transplant) -> Dict:
    dictionary = {
        "donor": transplant.donor.identifier,
        "recipient": transplant.recipient.identifier,
        "score": transplant.score
    }
    return dictionary
