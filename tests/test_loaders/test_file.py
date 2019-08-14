import unittest
from pathlib import Path

import jinete as jit


class TestFileLoader(unittest.TestCase):
    file_path: Path

    @classmethod
    def setUpClass(cls) -> None:
        cls.directory_path = Path('/tmp/')
        cls.file_path = cls.directory_path / 'jinete_problem_test.txt'
        cls.data = (
            (1.0, 1, 480, 6.0, 90.0),
            (0.0, -1.044, 2.000, 0.0, 0.0, 0.0, 1440.0),
            (1.0, -2.973, 6.414, 10.0, 1.0, 0.0, 1440.0),
            (2.0, -5.476, 1.437, 10.0, -1.0, 258.0, 287.0),
        )
        with cls.file_path.open('w') as file:
            file.writelines('\t'.join(map(str, row)) + '\n' for row in cls.data)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.file_path.unlink()

    def test_creation(self):
        loader = jit.FileLoader(
            file_path=self.file_path,
        )
        self.assertEqual(loader.file_path, self.file_path)
        self.assertEqual(loader.data, self.data)
        self.assertEqual(jit.Fleet, loader.fleet.__class__)
        self.assertEqual(jit.Job, loader.job.__class__)
        self.assertEqual(jit.GeometricSurface, loader.surface.__class__)

    if __name__ == '__main__':
        unittest.main()
