from __future__ import annotations

import unittest
from abc import ABC
from typing import TYPE_CHECKING

import jinete as jit

if TYPE_CHECKING:
    pass


class TestObjective(unittest.TestCase, ABC):
    planned_trip: jit.PlannedTrip
    stop: jit.Stop
    route: jit.Route
    planning: jit.Planning
    result: jit.Result

    @classmethod
    def setUpClass(cls) -> None:
        surface = jit.GeometricSurface(jit.DistanceMetric.MANHATTAN)
        origin = jit.Service(surface.get_or_create_position([0, 0]))
        vehicle = jit.Vehicle(identifier="TEST", origin=origin,)
        fleet = jit.Fleet({vehicle})

        trips = [
            jit.Trip(
                identifier="TEST_1",
                origin=jit.Service(position=surface.get_or_create_position([0, 0]), earliest=0.0, latest=10.0,),
                destination=jit.Service(position=surface.get_or_create_position([1, 1]),),
            ),
            jit.Trip(
                identifier="TEST_2",
                origin=jit.Service(position=surface.get_or_create_position([1, 1]), earliest=0.0, latest=20.0,),
                destination=jit.Service(position=surface.get_or_create_position([10, 10]),),
            ),
        ]
        job = jit.Job(set(trips), jit.DialARideObjective)
        route = jit.Route(vehicle)

        pickup_stop = jit.Stop(vehicle, surface.get_or_create_position([0, 0]), route.current_stop)
        delivery_stop = jit.Stop(vehicle, surface.get_or_create_position([1, 1]), pickup_stop)

        cls.planned_trip = jit.PlannedTrip(vehicle=vehicle, trip=trips[0], pickup=pickup_stop, delivery=delivery_stop,)
        route.append_planned_trip(cls.planned_trip)

        cls.stop = route.stops[1]
        conjecture = jit.TailInsertionStrategy()
        cls.route = conjecture.compute(route, trips[1])[0]
        cls.planning = jit.Planning({cls.route})
        cls.algorithm = jit.NaiveAlgorithm(fleet, job)
        cls.result = jit.Result(cls.algorithm, cls.planning, 0.0)
