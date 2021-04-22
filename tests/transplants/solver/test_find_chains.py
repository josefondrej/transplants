from typing import Tuple, List
from unittest import TestCase

import numpy as np

from transplants.solver.matching_from_matrix import _find_chains

_expected_chain_type = List[Tuple[List[int], bool]]

cyc = True
seq = False


class FindChainsTest(TestCase):
    @staticmethod
    def to_edges(string: str) -> List[Tuple[int, int]]:
        str_edges = string.split("|")
        str_edges = map(str.strip, str_edges)
        str_edges = [str_edge.replace(" ", "") for str_edge in str_edges]
        edges = [tuple(map(int, str_edge.split("->"))) for str_edge in str_edges]
        return edges

    @staticmethod
    def standardize_chain(chain: Tuple[List[int], bool]) -> Tuple[List[int], bool]:
        vertices, is_cycle = chain
        if is_cycle:
            start_index = np.argmin(vertices)
            vertices = vertices[start_index:] + vertices[:start_index]
        return vertices, is_cycle

    def assert_solver_result(self, graph_description: str, expected_chains: _expected_chain_type):
        graph_edges = self.to_edges(graph_description)
        calculated_chains = _find_chains(graph_edges)

        expected_chains = list(map(self.standardize_chain, expected_chains))
        calculated_chains = list(map(self.standardize_chain, calculated_chains))

        self.assertCountEqual(expected_chains, calculated_chains)

    def test_1_cycle(self):
        self.assert_solver_result(
            graph_description="1 -> 2 | 2 -> 3 | 3 -> 4 | 4 -> 1",
            expected_chains=[([1, 2, 3, 4], cyc)]
        )

    def test_4_cycles(self):
        self.assert_solver_result(
            graph_description="1 -> 2 | 2 -> 1 | 3 -> 4 | 4 -> 3 | 5 -> 6 | 6 -> 7 | 7 -> 8 | 8 -> 5 | 9 -> 10 | 10 -> 11 | 11 -> 9",
            expected_chains=[([1, 2], cyc), ([3, 4], cyc), ([5, 6, 7, 8], cyc), ([9, 10, 11], cyc)]
        )

    def test_1_sequence(self):
        self.assert_solver_result(
            graph_description="1 -> 2 | 2 -> 3 | 3 -> 4 | 4 -> 5",
            expected_chains=[([1, 2, 3, 4, 5], seq)]
        )

    def test_4_sequences(self):
        self.assert_solver_result(
            graph_description="1 -> 2 | 3 -> 4 | 5 -> 6 | 6 -> 7 | 8 -> 9 | 9 -> 10 | 10 -> 11",
            expected_chains=[([1, 2], seq), ([3, 4], seq), ([5, 6, 7], seq), ([8, 9, 10, 11], seq)]
        )

    def test_1_cycle_1_sequence(self):
        self.assert_solver_result(
            graph_description="1 -> 2 | 2 -> 3 | 3 -> 4 | 4 -> 1 | 5 -> 6 | 6 -> 7 | 7 -> 8",
            expected_chains=[([1, 2, 3, 4], cyc), ([5, 6, 7, 8], seq)]
        )

    def test_2_cycles_1_sequence(self):
        self.assert_solver_result(
            graph_description="1 -> 2 | 2 -> 3 | 3 -> 1 | 4 -> 5 | 5 -> 4 | 6 -> 7",
            expected_chains=[([1, 2, 3], cyc), ([4, 5], cyc), ([6, 7], seq)]
        )

    def test_1_cycle_2_sequences(self):
        self.assert_solver_result(
            graph_description="1 -> 2 | 2 -> 3 | 3 -> 1 | 4 -> 5 | 6 -> 7 | 7 -> 8 | 8 -> 9",
            expected_chains=[([1, 2, 3], cyc), ([4, 5], seq), ([6, 7, 8, 9], seq)]
        )

    def test_4_cycles_4_sequences(self):
        self.assert_solver_result(
            graph_description="1 -> 2 | 2 -> 1 | 3 -> 4 | 4 -> 3 | 5 -> 6 | 6 -> 7 | 7 -> 8 | 8 -> 5 | 9 -> 10 | 10 -> 11 | 11 -> 9 "
                              "| 100 -> 200 | 300 -> 400 | 500 -> 600 | 600 -> 700 | 800 -> 900 | 900 -> 1000 | 1000 -> 1100",
            expected_chains=[([1, 2], cyc), ([3, 4], cyc), ([5, 6, 7, 8], cyc), ([9, 10, 11], cyc),
                             ([100, 200], seq), ([300, 400], seq), ([500, 600, 700], seq),
                             ([800, 900, 1000, 1100], seq)]
        )
