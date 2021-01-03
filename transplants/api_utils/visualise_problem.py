import itertools
import json
import os
from typing import List, Optional, Tuple, Any

import matplotlib.cm
import matplotlib.pyplot as plt
import networkx as nx
from networkx import Graph

from transplants.api_utils.patients_from_params import patients_from_params
from transplants.api_utils.scorer_from_params import scorer_from_params
from transplants.core.patient.donor import Donor
from transplants.core.patient.recipient import Recipient
from transplants.core.scorer.additive_scorer_base import AdditiveScorerBase
from transplants.core.scorer.scorer_base import TRANSPLANT_IMPOSSIBLE
from transplants.core.solution.matching import Matching
from transplants.core.solution.transplant import Transplant
from transplants.core.solver.or_tools_solver import ORToolsSolver


def _get_node_attribute(graph: Graph, node: str, attribute_name: str) -> Any:
    attribute_value = graph.nodes[node].get(attribute_name)
    return attribute_value


def _set_node_attribute(graph: Graph, node: str, **attribute_names_values):
    for key, value in attribute_names_values.items():
        graph.nodes[node][key] = value


def _set_edge_attribute(graph: Graph, edge: Tuple[str, str], **attribute_names_values):
    for key, value in attribute_names_values.items():
        graph.edges[edge][key] = value


def _get_edge_attribute(graph: Graph, edge: Tuple[str, str], attribute_name: str):
    attribute_value = graph.edges[edge].get(attribute_name)
    return attribute_value


def _build_networkx_graph(donors: List[Donor], recipients: List[Recipient], scorer: AdditiveScorerBase) -> Graph:
    """Add edges from donors to recipients and from recipients to their related donors"""
    graph = nx.Graph()
    for patient in donors + recipients:
        graph.add_node(patient.identifier, is_donor=patient.is_donor)

    for donor in donors:
        for recipient in recipients:
            score = scorer.score_transplant(Transplant(donor=donor, recipient=recipient))
            if score != TRANSPLANT_IMPOSSIBLE:
                graph.add_edge(donor.identifier, recipient.identifier, score=score, is_transplant=True)

    for recipient in recipients:
        for donor in recipient.related_donors:
            graph.add_edge(recipient.identifier, donor.identifier, is_transplant=False)

    return graph


def _color_nodes(graph: Graph, donor_color: str = "#66c0ed", recipient_color: str = "#ed66eb"):
    for node in graph.nodes:
        is_donor = _get_node_attribute(graph, node, "is_donor")
        color = donor_color if is_donor else recipient_color
        _set_node_attribute(graph, node, color=color)


def _style_edges(graph: Graph, make_transplants_transparent: bool = False):
    edge_color_map = matplotlib.cm.get_cmap('Greys')
    max_score = max(nx.get_edge_attributes(graph, "score").values())

    for edge in graph.edges:
        is_transplant = _get_edge_attribute(graph, edge, "is_transplant")
        if is_transplant:
            score = _get_edge_attribute(graph, edge, "score")
            normalized_score = score / max_score
            if make_transplants_transparent:
                color = (0, 0, 0, 0)
            else:
                color = edge_color_map(normalized_score + 0.3)
            line_style = "solid"
        else:
            color = "gray"
            line_style = "dashed"

        _set_edge_attribute(graph, edge, color=color, line_style=line_style, line_width=1.0)


def _highlight_solution(graph: Graph, solution: Matching, chain_colors: List[str] = None,
                        line_width: float = 2.5):
    if chain_colors is None:
        chain_colors = ["#BF37BF", "#AE4FFF", "#917AFF", "#A7BAFF", "#D8F1FF", "#80215F"]

    for chain, chain_color in zip(solution.chains, itertools.cycle(chain_colors)):
        first_node = chain.transplants[0].donor.identifier
        _set_node_attribute(graph, first_node, color=chain_color)

        for transplant in chain.transplants:
            edge = (transplant.donor.identifier, transplant.recipient.identifier)
            score = _get_edge_attribute(graph, edge, "score")
            _set_edge_attribute(graph, edge, color=chain_color, line_width=line_width, label=score)

            next_transplant = chain.next_transplant(transplant)
            if next_transplant is not None:
                edge = (transplant.recipient.identifier, next_transplant.donor.identifier)
                _set_edge_attribute(graph, edge, color=chain_color, line_width=line_width)


def visualise_problem(donors: List[Donor], recipients: List[Recipient], scorer: AdditiveScorerBase,
                      solution: Optional[Matching], align: str = "vertical",
                      make_transplants_transparent: bool = False):
    graph = _build_networkx_graph(donors=donors, recipients=recipients, scorer=scorer)
    _color_nodes(graph)
    _style_edges(graph, make_transplants_transparent=make_transplants_transparent)
    _highlight_solution(graph, solution)

    pos = dict()
    pos.update({donor.identifier: [0, i] for i, donor in enumerate(donors)})
    pos.update({recipient.identifier: [1, i] for i, recipient in enumerate(recipients)})

    if align == "horizontal":
        pos = {node: [j, 1 - i] for node, (i, j) in pos.items()}

    nx.draw(
        G=graph,
        pos=pos,
        with_labels=True,
        node_color=[_get_node_attribute(graph, node, "color") for node in graph.nodes],
        edge_color=[_get_edge_attribute(graph, edge, "color") for edge in graph.edges],
        node_size=1000,
        width=[_get_edge_attribute(graph, edge, "line_width") for edge in graph.edges],
        style=[_get_edge_attribute(graph, edge, "line_style") for edge in graph.edges],
        labels={node: str(node)[-3:] for node in graph.nodes},
        node_shape="h"
    )

    # Draw label at 2 places on each line to avoid crossing lines covering each others label
    for label_pos in [0.15, 0.85]:
        nx.draw_networkx_edge_labels(
            G=graph,
            pos=pos,
            edge_labels=nx.get_edge_attributes(graph, "label"),
            label_pos=label_pos,
            alpha=0.8
        )


if __name__ == '__main__':
    # Load patients, scorer & solver and use it to get a solution ------------------------------------------------------
    patients_data_path = "./test/test_utils/test_patient_pool.json"

    with open(patients_data_path, "r") as patients_data_file:
        serialized_patients = json.load(patients_data_file)

    scorer_parameters = {
        "type": "HLABloodTypeAdditiveScorer",
        "compatible_blood_group_bonus": 0.0,
        "incompatible_blood_group_malus": float("-inf"),
        "hla_allele_compatibility_bonus": {"A": 1.0, "B": 3.0, "DRB1": 9.0},
        "max_allowed_antibody_concentration": {},
        "forbidden_transplants": [],
        "min_required_base_score": 0.0
    }

    test_donors, test_recipients = patients_from_params(serialized_patients=serialized_patients)
    test_scorer = scorer_from_params(
        scorer_parameters=scorer_parameters,
        patients=test_donors + test_recipients,
        add_related_to_forbidden=True
    )
    test_solver = ORToolsSolver()
    matchings = test_solver.solve(
        donors=set(test_donors),
        recipients=set(test_recipients),
        scorer=test_scorer
    )
    test_solution = matchings[0]

    # Export solution to /tmp/transplants/problem_visualisation.pdf ----------------------------------------------------
    os.makedirs("/tmp/transplants/", exist_ok=True)
    plt.figure(figsize=(20, 10))

    visualise_problem(
        donors=test_donors,
        recipients=test_recipients,
        scorer=test_scorer,
        solution=test_solution,
        align="horizontal",
        make_transplants_transparent=True
    )

    plt.savefig("/tmp/transplants/problem_visualisation.pdf")
