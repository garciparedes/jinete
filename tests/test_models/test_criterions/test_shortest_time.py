import unittest

import jinete as jit


class TestShortestTimePlannedTripCriterion(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        surface = jit.GeometricSurface(jit.DistanceMetric.MANHATTAN)
        vehicle = jit.Vehicle(
            identifier='TEST',
            initial=surface.get_or_create_position([0, 0]),
        )
        route = jit.Route(vehicle)
        cls.planned_trips = [
            jit.PlannedTrip(
                route=route,
                trip=jit.Trip(
                    identifier='TEST_1',
                    origin=surface.get_or_create_position([0, 0]),
                    destination=surface.get_or_create_position([1, 1]),
                    earliest=0.0,
                    timeout=10.0,
                ),
                collection_time=0.0,
                delivery_time=2.0
            ),
            jit.PlannedTrip(
                route=route,
                trip=jit.Trip(
                    identifier='TEST_1',
                    origin=surface.get_or_create_position([1, 1]),
                    destination=surface.get_or_create_position([10, 10]),
                    earliest=0.0,
                    timeout=10.0,
                ),
                collection_time=2.0,
                delivery_time=20.0
            )
        ]

    def test_creation(self):
        criterion = jit.ShortestTimePlannedTripCriterion()
        self.assertEqual(jit.OptimizationDirection.MINIMIZATION, criterion.direction)
        self.assertEqual('Shortest-Time', criterion.name)

    def test_sorting(self):
        criterion = jit.ShortestTimePlannedTripCriterion()

        self.assertEqual(
            self.planned_trips,
            criterion.sorted(reversed(self.planned_trips)),
        )

    def test_scoring(self):
        criterion = jit.ShortestTimePlannedTripCriterion()

        self.assertEqual(
            2.0,
            criterion.scoring(self.planned_trips[0]),
        )

        self.assertEqual(
            20.0,
            criterion.scoring(self.planned_trips[1]),
        )

    def test_best(self):
        criterion = jit.ShortestTimePlannedTripCriterion()

        self.assertEqual(
            self.planned_trips[0],
            criterion.best(*self.planned_trips),
        )


if __name__ == '__main__':
    unittest.main()
