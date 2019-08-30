import unittest

import jinete as jit
from ...utils import (
    generate_one_result,
)


class TestHashCodeStorerFormatter(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.result = generate_one_result()
        cls.expected_result = '\n'.join([
            '2 0 1',
            '1 2',
        ])

    def test_creation(self):
        storer = jit.HashCodeStorerFormatter(self.result)
        self.assertEqual(self.expected_result, storer.format())


if __name__ == '__main__':
    unittest.main()
