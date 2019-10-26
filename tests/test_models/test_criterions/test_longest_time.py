from __future__ import annotations

import unittest
from typing import TYPE_CHECKING
import jinete as jit

if TYPE_CHECKING:
    from typing import (
        List,
    )


class TestLongestTimePlannedTripCriterion(unittest.TestCase):
    planned_trips: List[jit.PlannedTrip]

    @classmethod
    def setUpClass(cls) -> None:
        surface = jit.GeometricSurface(jit.DistanceMetric.MANHATTAN)
        origin = jit.Service(surface.get_or_create_position([0, 0]))
        vehicle = jit.Vehicle(
            identifier='TEST',
            origin=origin,
        )
        route = jit.Route(vehicle)
        pickup_stop_1 = jit.Stop(route, surface.get_or_create_position([0, 0]), route.last_stop)
        delivery_stop_1 = jit.Stop(route, surface.get_or_create_position([1, 1]), pickup_stop_1)

        pickup_stop_2 = jit.Stop(route, surface.get_or_create_position([0, 0]), route.last_stop)
        delivery_stop_2 = jit.Stop(route, surface.get_or_create_position([10, 10]), pickup_stop_2)

        cls.planned_trips = [
            jit.PlannedTrip(
                route=route,
                trip=jit.Trip(
                    identifier='TEST_1',
                    origin=jit.Service(
                        position=surface.get_or_create_position([0, 0]),
                        earliest=0.0,
                        latest=10.0,
                    ),
                    destination=jit.Service(
                        position=surface.get_or_create_position([1, 1]),
                    ),
                ),
                pickup=pickup_stop_1,
                delivery=delivery_stop_1,
            ),
            jit.PlannedTrip(
                route=route,
                trip=jit.Trip(
                    identifier='TEST_1',
                    origin=jit.Service(
                        position=surface.get_or_create_position([0, 0]),
                        earliest=0.0,
                        latest=20.0,
                    ),
                    destination=jit.Service(
                        position=surface.get_or_create_position([10, 10]),
                    ),
                ),
                pickup=pickup_stop_2,
                delivery=delivery_stop_2,
            )
        ]

    def test_creation(self):
        criterion = jit.LongestTimePlannedTripCriterion()
        self.assertEqual(jit.OptimizationDirection.MAXIMIZATION, criterion.direction)
        self.assertEqual('Longest-Time', criterion.name)

    def test_sorting(self):
        criterion = jit.LongestTimePlannedTripCriterion()

        self.assertEqual(
            self.planned_trips[::-1],
            criterion.sorted(self.planned_trips),
        )

    def test_scoring(self):
        criterion = jit.LongestTimePlannedTripCriterion()

        self.assertEqual(
            2.0,
            criterion.scoring(self.planned_trips[0]),
        )

        self.assertEqual(
            20.0,
            criterion.scoring(self.planned_trips[1]),
        )

    def test_best(self):
        criterion = jit.LongestTimePlannedTripCriterion()

        self.assertEqual(
            self.planned_trips[1],
            criterion.best(*self.planned_trips),
        )


if __name__ == '__main__':
    unittest.main()
