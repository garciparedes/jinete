import unittest

import jinete as jit

from tests.utils import (
    generate_vehicles,
)


class TestFleet(unittest.TestCase):

    def test_construction(self):
        vehicles = generate_vehicles(3)
        fleet = jit.Fleet(vehicles)

        self.assertIsInstance(fleet, jit.Fleet)
        self.assertEqual(fleet.vehicles, vehicles)

    def test_as_tuple(self):
        vehicles = generate_vehicles(3)
        fleet = jit.Fleet(vehicles)

        expected = (
            ('vehicle_identifiers', tuple(vehicle.identifier for vehicle in vehicles)),
        )
        self.assertEqual(expected, tuple(fleet))


if __name__ == '__main__':
    unittest.main()
