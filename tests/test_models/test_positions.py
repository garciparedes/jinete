import unittest

import jinete as jit
from tests.utils import generate_one_surface


class TestPositions(unittest.TestCase):

    def test_xy_position(self):
        surface = generate_one_surface()
        position = jit.GeometricPosition([3, 4], surface)
        self.assertEqual(3, position[0])
        self.assertEqual(4, position[1])


if __name__ == '__main__':
    unittest.main()
