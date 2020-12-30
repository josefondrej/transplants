from typing import Tuple, List
from unittest import TestCase
import numpy as np

from transplants.core.solver.find_chains import find_chains


class FindChainsTest(TestCase):
    def setUp(self) -> None:
        # test_case = (
        #   "i -> j" -- transplant(i -> j) is performed OR j in i.related_donors
        #   [([i,j,k], is_cycle), ([l,m], is_cycle)] -- cycles or sequences of vertices in the graph given by ^^
        # )
        cyc = True
        seq = False

        self.test_cases = dict(
            cycle_1=(
                "1 -> 2 | 2 -> 3 | 3 -> 4 | 4 -> 1",
                [([1, 2, 3, 4], cyc)]
            ),
            cycle_4=(
                "1 -> 2 | 2 -> 1 | 3 -> 4 | 4 -> 3 | 5 -> 6 | 6 -> 7 | 7 -> 8 | 8 -> 5 | 9 -> 10 | 10 -> 11 | 11 -> 9",
                [([1, 2], cyc), ([3, 4], cyc), ([5, 6, 7, 8], cyc), ([9, 10, 11], cyc)]
            ),
            sequence_1=(
                "1 -> 2 | 2 -> 3 | 3 -> 4 | 4 -> 5",
                [([1, 2, 3, 4, 5], seq)]
            ),
            sequence_4=(
                "1 -> 2 | 3 -> 4 | 5 -> 6 | 6 -> 7 | 8 -> 9 | 9 -> 10 | 10 -> 11",
                [([1, 2], seq), ([3, 4], seq), ([5, 6, 7], seq), ([8, 9, 10, 11], seq)]
            ),
            cycle_1_sequence_1=(
                "1 -> 2 | 2 -> 3 | 3 -> 4 | 4 -> 1 | 5 -> 6 | 6 -> 7 | 7 -> 8",
                [([1, 2, 3, 4], cyc), ([5, 6, 7, 8], seq)]
            ),
            cycle_2_sequence_1=(
                "1 -> 2 | 2 -> 3 | 3 -> 1 | 4 -> 5 | 5 -> 4 | 6 -> 7",
                [([1, 2, 3], cyc), ([4, 5], cyc), ([6, 7], seq)]
            ),
            cycle_1_sequence_2=(
                "1 -> 2 | 2 -> 3 | 3 -> 1 | 4 -> 5 | 6 -> 7 | 7 -> 8 | 8 -> 9",
                [([1, 2, 3], cyc), ([4, 5], seq), ([6, 7, 8, 9], seq)]
            ),
            cycle_4_sequence_4=(
                "1 -> 2 | 2 -> 1 | 3 -> 4 | 4 -> 3 | 5 -> 6 | 6 -> 7 | 7 -> 8 | 8 -> 5 | 9 -> 10 | 10 -> 11 | 11 -> 9 "
                "| 100 -> 200 | 300 -> 400 | 500 -> 600 | 600 -> 700 | 800 -> 900 | 900 -> 1000 | 1000 -> 1100",
                [([1, 2], cyc), ([3, 4], cyc), ([5, 6, 7, 8], cyc), ([9, 10, 11], cyc),
                 ([100, 200], seq), ([300, 400], seq), ([500, 600, 700], seq), ([800, 900, 1000, 1100], seq)]
            )
        )

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

    def test_find_test(self):
        for test_case_name, test_case in self.test_cases.items():
            graph_description, expected_chains = test_case
            graph_edges = FindChainsTest.to_edges(graph_description)
            calculated_chains = find_chains(graph_edges)

            expected_chains = list(map(FindChainsTest.standardize_chain, expected_chains))
            calculated_chains = list(map(FindChainsTest.standardize_chain, calculated_chains))

            self.assertCountEqual(expected_chains, calculated_chains)
            print(f"{test_case_name} ok")
