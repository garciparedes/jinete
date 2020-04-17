from __future__ import annotations

import unittest
from typing import TYPE_CHECKING
import itertools as it

import jinete as jit

from tests.utils import (
    generate_one_vehicle,
    generate_one_position,
    generate_one_planned_trip,
)

if TYPE_CHECKING:
    from typing import List


class TestStop(unittest.TestCase):
    vehicle: jit.Vehicle
    position: jit.Position
    stops: List[jit.Stop]

    @classmethod
    def setUpClass(cls) -> None:
        cls.vehicle = generate_one_vehicle()
        cls.position = generate_one_position()

    def setUp(self) -> None:
        stop0 = jit.Stop(self.vehicle, self.position, None)

        stop1 = jit.Stop(self.vehicle, generate_one_position(), stop0)
        stop0.following = stop1

        stop2 = jit.Stop(self.vehicle, generate_one_position(), stop1)
        stop1.following = stop2

        stop3 = jit.Stop(self.vehicle, generate_one_position(), stop2)
        stop2.following = stop3

        stop4 = jit.Stop(self.vehicle, generate_one_position(), stop3)
        stop3.following = stop4

        stops = [stop0, stop1, stop2, stop3, stop4]
        self.stops = stops

    def test_creation(self):
        stop = jit.Stop(self.vehicle, self.position, None)

        self.assertNotIn("arrival_time", stop.__dict__)
        self.assertNotIn("departure_time", stop.__dict__)

        self.assertEqual(self.vehicle, stop.vehicle)
        self.assertEqual(self.position, stop.position)
        self.assertIsNone(stop.previous)
        self.assertEqual(self.vehicle.origin_position, stop.previous_position)
        self.assertEqual(self.vehicle.origin_earliest, stop.previous_departure_time)
        self.assertEqual(
            stop.position.time_to(self.vehicle.origin_position, stop.previous_departure_time), stop.transit_time,
        )
        self.assertEqual(0, stop.waiting_time)
        self.assertEqual(0, stop.load_time)
        self.assertEqual(0, len(tuple(stop.planned_trips)))
        self.assertEqual(0, len(tuple(stop.trips)))

    def test_creation_with_previous(self):
        previous_position = generate_one_position()
        previous_stop = jit.Stop(self.vehicle, previous_position, None)

        stop = jit.Stop(self.vehicle, self.position, previous_stop)
        previous_stop.following = stop

        self.assertEqual(previous_stop.following, stop)
        self.assertEqual(self.vehicle, stop.vehicle)
        self.assertEqual(self.position, stop.position)
        self.assertEqual(previous_stop, stop.previous)
        self.assertEqual(stop.position.distance_to(previous_stop.position), stop.distance)
        self.assertEqual(previous_stop.position, stop.previous_position)
        self.assertEqual(previous_stop.departure_time, stop.previous_departure_time)
        self.assertEqual(
            stop.position.time_to(previous_stop.position, stop.previous_departure_time), stop.transit_time,
        )

    def test_flush(self):
        stop = jit.Stop(self.vehicle, self.position, None)

        self.assertNotIn("arrival_time", stop.__dict__)
        self.assertNotIn("departure_time", stop.__dict__)

        self.assertIsInstance(stop.departure_time, float)

        self.assertIn("arrival_time", stop.__dict__)
        self.assertIn("departure_time", stop.__dict__)

        stop.flush()

        self.assertNotIn("arrival_time", stop.__dict__)
        self.assertNotIn("departure_time", stop.__dict__)

    def test_cache(self):
        self.assertIsInstance(self.stops[-1].departure_time, float)
        for stop in self.stops:
            self.assertIn("arrival_time", stop.__dict__)
            self.assertIn("departure_time", stop.__dict__)

    def test_all_previous(self):
        self.assertIsInstance(self.stops[-1].departure_time, float)

        self.stops[2].flush_all_previous()

        for stop in self.stops[:3]:
            self.assertNotIn("arrival_time", stop.__dict__)
            self.assertNotIn("departure_time", stop.__dict__)

        for stop in self.stops[3:]:
            self.assertIn("arrival_time", stop.__dict__)
            self.assertIn("departure_time", stop.__dict__)

    def test_with_planned_trip(self):
        stop = jit.Stop(self.vehicle, self.position, self.stops[0])

        delivery_planned_trip = generate_one_planned_trip(
            feasible=True, vehicle=self.vehicle, pickup_stop=self.stops[0], delivery_stop=stop,
        )

        pickup_planned_trip = generate_one_planned_trip(feasible=True, vehicle=self.vehicle, pickup_stop=stop,)
        self.assertIn(delivery_planned_trip, stop.delivery_planned_trips)
        self.assertNotIn(delivery_planned_trip, stop.pickup_planned_trips)

        self.assertNotIn(pickup_planned_trip, stop.delivery_planned_trips)
        self.assertIn(pickup_planned_trip, stop.pickup_planned_trips)
        self.assertIsInstance(stop.identifier, str)

        iterable = it.chain(
            (f"P{planned_trip.trip_identifier}" for planned_trip in stop.pickup_planned_trips),
            (f"D{planned_trip.trip_identifier}" for planned_trip in stop.delivery_planned_trips),
        )
        identifier = "|".join(iterable)
        identifier = f"[{identifier}]"
        self.assertEqual(identifier, stop.identifier)


if __name__ == "__main__":
    unittest.main()
