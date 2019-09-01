import unittest
from copy import deepcopy

import jinete as jit
from tests.utils import (
    generate_one_surface,
    generate_one_position,
)


class TestGeometricPosition(unittest.TestCase):

    def test_construction(self):
        surface = generate_one_surface()
        position = jit.GeometricPosition([3, 4], surface)
        self.assertEqual(3, position[0])
        self.assertEqual(4, position[1])

    def test_deepcopy(self):
        position = generate_one_position()
        copied_position = deepcopy(position)
        self.assertEqual(position, copied_position)


if __name__ == '__main__':
    unittest.main()
