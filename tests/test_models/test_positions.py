import unittest

import jinete as jit


class TestPositions(unittest.TestCase):

    def test_xy_position(self):
        position = jit.GeometricPosition([3, 4])
        self.assertEqual(3, position[0])
        self.assertEqual(4, position[1])


if __name__ == '__main__':
    unittest.main()
