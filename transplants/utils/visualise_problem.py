import itertools
import os
from typing import List, Optional, Tuple, Any

import matplotlib.cm
import matplotlib.pyplot as plt
import networkx as nx
from networkx import Graph

from transplants.problem.patient.donor import Donor
from transplants.problem.patient.recipient import Recipient
from transplants.problem.problem import Problem
from transplants.solution.matching import Matching
from transplants.solution.transplant import Transplant
from transplants.solver.or_tools_solver import ORToolsSolver
from transplants.solver.scorer.additive_scorer_base import AdditiveScorerBase
from transplants.solver.scorer.default_forbidden_transplants import get_default_forbidden_transplants
from transplants.solver.scorer.hla_blood_type_additive_scorer import HLABloodTypeAdditiveScorer
from transplants.solver.scorer.scorer_base import TRANSPLANT_IMPOSSIBLE
from transplants.utils.load_donors_recipients import load_donors_recipients_from_file
from transplants.utils.paths import get_abs_path


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
            score = scorer.score_transplant(Transplant(donor_id=donor.identifier, recipient_id=recipient.identifier))
            if score != TRANSPLANT_IMPOSSIBLE:
                graph.add_edge(donor.identifier, recipient.identifier, score=score, is_transplant=True)

    for recipient in recipients:
        for donor_id in recipient.related_donor_ids:
            graph.add_edge(recipient.identifier, donor_id, is_transplant=False)

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
        first_node = chain.transplants[0].donor_id
        _set_node_attribute(graph, first_node, color=chain_color)

        for transplant in chain.transplants:
            edge = (transplant.donor_id, transplant.recipient_id)
            score = _get_edge_attribute(graph, edge, "score")
            _set_edge_attribute(graph, edge, color=chain_color, line_width=line_width, label=score)

            next_transplant = chain.next_transplant(transplant)
            if next_transplant is not None:
                edge = (transplant.recipient_id, next_transplant.donor_id)
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
    # Patients
    test_donors, test_recipients = load_donors_recipients_from_file(
        get_abs_path("test/test_utils/patient_pool_example.json"))
    test_patients = test_donors + test_recipients
    test_problem = Problem(problem_id="test_problem_id", patients=test_patients)

    # Scorer
    forbidden_transplants = get_default_forbidden_transplants(patients=test_patients)
    test_scorer = HLABloodTypeAdditiveScorer(
        problem=test_problem,
        compatible_blood_group_bonus=0.0,
        forbidden_transplants=forbidden_transplants
    )

    # Solver
    test_solver = ORToolsSolver(scorer=test_scorer)

    # Find exchanges
    solution = test_solver.solve(
        problem=test_problem
    )

    matchings = solution.matchings
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
