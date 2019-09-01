import unittest
from pathlib import Path
from unittest.mock import patch

import networkx as nx

import jinete as jit

from tests.utils import (
    generate_one_result,
)


class TestGraphPlotStorer(unittest.TestCase):
    directory_path: Path
    result: jit.Result

    @classmethod
    def setUpClass(cls) -> None:
        cls.directory_path = Path('/tmp/')
        cls.result = generate_one_result()

    def test_creation(self):
        storer = jit.GraphPlotStorer(
            result=self.result,
        )
        self.assertEqual(storer.result, self.result)

    @patch("jinete.storers.plots.graph.plt.show")
    def test_store(self, mocked_plt):
        storer = jit.GraphPlotStorer(
            result=self.result,
        )
        graph = storer._generate_graph()
        self.assertIsInstance(graph, nx.DiGraph)

        storer.store()


if __name__ == '__main__':
    unittest.main()
