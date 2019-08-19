import unittest
from sys import maxsize

import jinete as jit


class TestConstants(unittest.TestCase):

    def test_max_int(self):
        self.assertEqual(jit.MAX_INT, maxsize)

    def test_min_int(self):
        self.assertEqual(jit.MIN_INT, -maxsize)

    def test_max_float(self):
        self.assertEqual(jit.MAX_FLOAT, float('inf'))

    def test_min_float(self):
        self.assertEqual(jit.MIN_FLOAT, float('-inf'))


if __name__ == '__main__':
    unittest.main()
