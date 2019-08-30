import unittest
from pathlib import Path

import networkx as nx

import jinete as jit

from tests.utils import (
    generate_one_result,
)


class TestGraphPlotStorer(unittest.TestCase):
    file_path: Path

    @classmethod
    def setUpClass(cls) -> None:
        cls.directory_path = Path('/tmp/')
        cls.result = generate_one_result()

    def test_creation(self):
        storer = jit.GraphPlotStorer(
            result=self.result,
        )
        self.assertEqual(storer.result, self.result)

    def test_store(self):
        storer = jit.GraphPlotStorer(
            result=self.result,
        )
        graph = storer._generate_graph()
        self.assertIsInstance(graph, nx.DiGraph)

        storer.store()


if __name__ == '__main__':
    unittest.main()
