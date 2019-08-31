import unittest

import jinete as jit
from tests.utils import (
    generate_one_result,
)


class TestHashCodeStorerFormatter(unittest.TestCase):
    result: jit.Result
    expected_result: str

    @classmethod
    def setUpClass(cls) -> None:
        cls.result = generate_one_result()
        cls.expected_result = '\n'.join([
            '1 2',
            '2 0 1',
        ])

    def test_creation(self):
        storer = jit.HashCodeStorerFormatter(result=self.result)
        self.assertEqual(self.expected_result, storer.format())


if __name__ == '__main__':
    unittest.main()
