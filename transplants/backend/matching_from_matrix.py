# Utility functions for finding cycles and sequences in a graph given by it's adjacency matrix
from typing import List, Tuple, Dict, Set, Union

import numpy as np

from transplants.model.chain import Chain
from transplants.model.cycle import Cycle
from transplants.model.donor import Donor
from transplants.model.patient import Patient
from transplants.model.problem import Problem
from transplants.model.recipient import Recipient
from transplants.model.sequence import Sequence
from transplants.model.solution import Matching
from transplants.model.transplant import Transplant


def _find_chains(edges: List[Tuple[int, int]]) -> List[Tuple[List[int], bool]]:
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


def _get_arguments_from_transplant_matrix_and_patients(transplant_matrix: np.ndarray, problem: Problem) \
        -> Tuple[List[Tuple[int, int]], Dict[int, Union[Donor, Recipient]]]:
    """
    Get arguments for function `find_chains`
    Args:
        transplant_matrix: transplant_matrix[i,j] = Indicator(transplant donors[i] -> recipients[j] is performed)
        problem:

    Returns:
        edges: edges of graph where edge between patients i -> j means either:
            - there was a transplant from patient i to patient j
            - or that patient j is related donor to patient i AND that patient j leads to some transplant
        vertex_to_patient: Dict[int, Patient]
    """
    donors = problem.donors
    recipients = problem.recipients
    vertex_to_patient = {pat_ix: patient for pat_ix, patient in enumerate(donors + recipients)}
    patient_to_vertex: Dict[Patient, int] = {patient: pat_ix for pat_ix, patient
                                             in vertex_to_patient.items()}

    transplant_donor_recipient_indices = list(zip(*np.where(transplant_matrix)))
    transplants = [(donors[donor_ix], recipients[recipient_ix]) for donor_ix, recipient_ix
                   in transplant_donor_recipient_indices]
    was_used = {donor: True for donor, recipient in transplants}

    transplant_edges = [(patient_to_vertex[donor], patient_to_vertex[recipient]) for donor, recipient in
                        transplants]

    related_donor_edges = [(patient_to_vertex[recipient], patient_to_vertex[problem.get_patient(donor_id)])
                           for recipient in recipients
                           for donor_id in recipient.related_donor_ids
                           if was_used.get(problem.get_patient(donor_id))]

    edges = transplant_edges + related_donor_edges
    return edges, vertex_to_patient


def _index_chains_to_patient_chains(index_chains: List[Tuple[List[int], bool]],
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
                    donor_id=vertex_to_patient[index_chain[2 * i]].identifier,
                    recipient_id=vertex_to_patient[index_chain[2 * i + 1]].identifier
                ) for i in range(len(index_chain) // 2)
            ]
        )
        patient_chains.add(chain)

    return patient_chains


def get_matching_from_transplant_matrix(transplant_matrix: np.ndarray, problem: Problem) -> Matching:
    """Gets Matching from transplant matrix

    Args:

        transplant_matrix (np.array(int64)): can have values 0 / 1
            transplant_matrix[i,j] = 1 means transplant from donor i to recipient j is performed
            transplant_matrix[i,j] = 0 means transplant from donor i to recipient j is NOT performed
        problem: Problem containing the list of donors and list of recipients that are used to
            transform the indices to the actual patient ids in the resulting matching

    Returns: Matching containing the patient ids
    """
    edges, vertex_to_patient = _get_arguments_from_transplant_matrix_and_patients(
        transplant_matrix=transplant_matrix,
        problem=problem
    )
    index_chains = _find_chains(edges=edges)
    patient_chains = _index_chains_to_patient_chains(
        index_chains=index_chains,
        vertex_to_patient=vertex_to_patient
    )
    return Matching(chains=patient_chains)
