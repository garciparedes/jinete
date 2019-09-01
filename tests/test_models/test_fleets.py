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

    def test_as_dict(self):
        vehicles = generate_vehicles(3)
        fleet = jit.Fleet(vehicles)

        vehicles_str = ', '.join(str(vehicle) for vehicle in vehicles)
        expected = {
            'vehicles': f'{{{vehicles_str}}}'
        }
        self.assertEqual(expected, fleet.as_dict())


if __name__ == '__main__':
    unittest.main()
