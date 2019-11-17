import unittest
from copy import deepcopy

import jinete as jit
from tests.utils import (
    generate_one_surface,
    generate_one_position,
)


class TestGeometricPosition(unittest.TestCase):

    def setUp(self) -> None:
        self.surface = generate_one_surface()

    def test_construction(self):
        coordinates = (3, 4,)
        position = jit.GeometricPosition(coordinates, self.surface)
        self.assertEqual(coordinates[0], position[0])
        self.assertEqual(coordinates[1], position[1])
        self.assertEqual(hash(coordinates), hash(position))

    def test_equality(self):
        coordinates = (1.1, 2.2,)

        a = jit.GeometricPosition(coordinates, self.surface)
        b = jit.GeometricPosition(coordinates, self.surface)

        self.assertEqual(a, b)

    def test_not_equality(self):
        a = jit.GeometricPosition([1.1, 2.2], self.surface)
        b = jit.GeometricPosition([3.3, 4.4], self.surface)

        self.assertNotEqual(a, b)

    def test_deepcopy(self):
        position = generate_one_position()
        copied_position = deepcopy(position)
        self.assertEqual(position, copied_position)

    def test_as_tuple(self):
        coordinates = (3, 4,)
        position = jit.GeometricPosition(coordinates, self.surface)

        expected = (
            ('coordinates', coordinates),
        )
        self.assertEqual(expected, tuple(position))

    def test_as_str(self):
        coordinates = (3, 4,)
        position = jit.GeometricPosition(coordinates, self.surface)

        expected = '(' + ",".join(f"{x:07.3f}" for x in coordinates) + ')'

        self.assertEqual(expected, str(position))


if __name__ == '__main__':
    unittest.main()
