import unittest

from uuid import UUID

import jinete as jit
from tests.utils import (
    generate_positions,
)


class TestSurfaces(unittest.TestCase):

    def test_geometric_surface(self):
        surface = jit.GeometricSurface(jit.DistanceMetric.EUCLIDEAN)
        positions = generate_positions(100, surface=surface)
        n = len(positions)
        self.assertIsInstance(surface.uuid, UUID)
        self.assertEqual(n, len(surface.positions))

    def test_distance(self):
        surface = jit.GeometricSurface(jit.DistanceMetric.EUCLIDEAN)
        positions = generate_positions(2, surface=surface)
        a, b = tuple(positions)
        real_dist = ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

        dist = surface.distance(a, b)
        self.assertAlmostEqual(dist, real_dist)


if __name__ == '__main__':
    unittest.main()
