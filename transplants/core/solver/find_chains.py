from typing import List, Tuple, Dict, Set, Union

import numpy as np

from transplants.core.patient.donor import Donor
from transplants.core.patient.recipient import Recipient
from transplants.core.solution.chain import Chain
from transplants.core.solution.cycle import Cycle
from transplants.core.solution.sequence import Sequence
from transplants.core.solution.transplant import Transplant


def find_chains(edges: List[Tuple[int, int]]) -> List[Tuple[List[int], bool]]:
    to_next = {i: j for i, j in edges}
    to_previous = {j: i for i, j in edges}
    vertices = set([v for edge in edges for v in edge])
    chains = list()
    while len(vertices) > 0:
        initial_vertex = vertices.pop()
        next_vertex = to_next.get(initial_vertex)
        prev_vertex = to_previous.get(initial_vertex)

        right_chain = list()
        left_chain = list()

        while next_vertex is not None and next_vertex != initial_vertex:
            right_chain.append(next_vertex)
            next_vertex = to_next.get(next_vertex)

        if next_vertex is None:
            is_cycle = False

            while prev_vertex is not None and prev_vertex != initial_vertex:
                left_chain.append(prev_vertex)
                prev_vertex = to_previous.get(prev_vertex)

        else:
            is_cycle = True

        chain = list(reversed(left_chain)) + [initial_vertex] + right_chain

        chains.append((chain, is_cycle))
        vertices -= set(chain)

    return chains


def get_arguments_from_transplant_matrix_and_patients(transplant_matrix: np.ndarray, donors: List[Donor],
                                                      recipients: List[Recipient]) \
        -> Tuple[List[Tuple[int, int]], Dict[int, Union[Donor, Recipient]]]:
    """
    Get arguments for function `find_chains`
    Args:
        transplant_matrix: transplant_matrix[i,j] = Indicator(transplant donors[i] -> recipients[j] is performed)
        donors: List of donors
        recipients: List of recipients

    Returns:
        edges: edges of graph where edge between patients i -> j means either:
            - there was a transplant from patient i to patient j
            - or that patient j is related donor to patient i AND that patient j leads to some transplant
        vertex_to_patient: Dict[int, Patient]
    """
    vertex_to_patient = {pat_ix: patient for pat_ix, patient in enumerate(donors + recipients)}
    patient_to_vertex: Dict[Union[Donor, Recipient], int] = {patient: pat_ix for pat_ix, patient in vertex_to_patient}

    transplant_donor_recipient_indices = list(np.zip(*np.where(transplant_matrix)))
    transplants = [(donors[donor_ix], recipients[recipient_ix]) for donor_ix, recipient_ix
                   in transplant_donor_recipient_indices]
    was_used = {donor: True for donor, recipient in transplants}

    transplant_edges = [(patient_to_vertex[donor], patient_to_vertex[recipient]) for donor, recipient in
                        transplants]

    related_donor_edges = [(patient_to_vertex[recipient], patient_to_vertex[donor])
                           for recipient in recipients
                           for donor in recipient.related_donors
                           if was_used.get(donor)]

    edges = transplant_edges + related_donor_edges
    return edges, vertex_to_patient


def index_chains_to_patient_chains(index_chains: Set[List[int]],
                                   vertex_to_patient: Dict[int, Union[Donor, Recipient]]) -> Set[Chain]:
    patient_chains = set()
    for index_chain, is_cycle in index_chains:
        # Ensure we always start the chain with donor -- this does not have to be so for cycles
        if vertex_to_patient[index_chain[0]].is_recipient:
            index_chain = index_chain[1:] + [index_chain[0]]

        chain_constructor = Cycle if is_cycle else Sequence
        chain = chain_constructor(
            transplants=[
                Transplant(
                    donor=vertex_to_patient[index_chain[2 * i]],
                    recipient=vertex_to_patient[index_chain[2 * i + 1]]
                ) for i in range(len(index_chain) // 2)
            ]
        )
        patient_chains.add(chain)

    return patient_chains
