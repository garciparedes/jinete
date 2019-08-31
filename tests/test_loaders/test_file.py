from __future__ import annotations

import unittest
from typing import TYPE_CHECKING
from pathlib import Path

import jinete as jit

if TYPE_CHECKING:
    from typing import (
        Sequence
    )


class TestFileLoader(unittest.TestCase):
    directory_path: Path
    file_path: Path
    data: Sequence[Sequence[float]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.directory_path = Path('/tmp/')
        cls.file_path = cls.directory_path / 'jinete_problem_test.txt'
        cls.data = [
            [1.0, 1, 480, 6.0, 90.0],
            [0.0, -1.044, 2.000, 0.0, 0.0, 0.0, 1440.0],
            [1.0, -2.973, 6.414, 10.0, 1.0, 0.0, 1440.0],
            [2.0, -5.476, 1.437, 10.0, -1.0, 258.0, 287.0],
        ]
        with cls.file_path.open('w') as file:
            file.writelines('\t'.join(str(cell) for cell in row) + '\n' for row in cls.data)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.file_path.unlink()

    def test_creation(self):
        loader = jit.FileLoader(
            file_path=self.file_path,
        )
        self.assertEqual(loader.file_path, self.file_path)
        self.assertEqual(loader.data, self.data)
        self.assertIsInstance(loader.fleet, jit.Fleet)
        self.assertIsInstance(loader.job, jit.Job)
        self.assertIsInstance(loader.surface, jit.GeometricSurface)


if __name__ == '__main__':
    unittest.main()
