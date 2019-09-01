import unittest
from pathlib import Path

import jinete as jit
from tests.utils import (
    generate_one_result,
)


class TestFileStorer(unittest.TestCase):
    directory_path: Path
    file_path: Path
    result: jit.Result

    @classmethod
    def setUpClass(cls) -> None:
        cls.directory_path = Path('/tmp/')
        cls.file_path = cls.directory_path / 'jinete_store_result_test.txt'
        cls.result = generate_one_result()

    @classmethod
    def tearDown(cls) -> None:
        if cls.file_path.exists():
            cls.file_path.unlink()

    def test_creation(self):
        storer = jit.FileStorer(
            file_path=self.file_path,
            result=self.result,
        )
        self.assertEqual(storer.file_path, self.file_path)
        self.assertEqual(storer.result, self.result)
        self.assertEqual(storer.formatter_cls, jit.ColumnarStorerFormatter)

    def test_store(self):
        storer = jit.FileStorer(
            file_path=self.file_path,
            result=self.result,
            formatter_cls=jit.HashCodeStorerFormatter,
        )
        storer.store()

        expected_result = '\n'.join([
            "1 2",
            "2 0 1",
        ])

        self.assertEqual(self.file_path.exists(), True)
        with self.file_path.open() as file:
            result = file.read()
            self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
