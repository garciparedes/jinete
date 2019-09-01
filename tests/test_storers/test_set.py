import unittest
from pathlib import Path
from unittest.mock import patch

import jinete as jit

from tests.utils import (
    generate_one_result,
)


class TestStorerSet(unittest.TestCase):
    directory_path: Path
    result: jit.Result

    @classmethod
    def setUpClass(cls) -> None:
        cls.directory_path = Path('/tmp/')
        cls.result = generate_one_result()

    def test_creation(self):
        storer_cls_set = {
            jit.PromptStorer,
            jit.GraphPlotStorer,
        }
        storer = jit.StorerSet(
            result=self.result,
            storer_cls_set=storer_cls_set,
        )
        self.assertEqual(storer.result, self.result)
        self.assertEqual(storer.storer_cls_set, storer_cls_set)

    @patch("jinete.storers.plots.graph.plt.show")
    def test_store(self, mocked_plt):
        storer = jit.StorerSet(
            result=self.result,
            storer_cls_set={
                jit.PromptStorer,
                jit.GraphPlotStorer,
            },
        )

        storer.store()


if __name__ == '__main__':
    unittest.main()
