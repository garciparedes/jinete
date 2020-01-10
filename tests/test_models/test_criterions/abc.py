from __future__ import annotations

import unittest
from abc import ABC
from typing import TYPE_CHECKING

import jinete as jit

if TYPE_CHECKING:
    from typing import (
        List,
    )


class TestRouteCriterion(unittest.TestCase, ABC):
    routes: List[jit.Route]

    @classmethod
    def setUpClass(cls) -> None:
        surface = jit.GeometricSurface(jit.DistanceMetric.MANHATTAN)
        origin = jit.Service(surface.get_or_create_position([0, 0]))
        vehicle = jit.Vehicle(
            identifier='TEST',
            origin=origin,
        )

        cls.routes = [
            cls._build_route_1(vehicle, surface),
            cls._build_route_2(vehicle, surface),
        ]

    @classmethod
    def _build_route_1(cls, vehicle: jit.Vehicle, surface: jit.Surface) -> jit.Route:
        route = jit.Route(vehicle)

        trip = jit.Trip(
            identifier='TEST_1',
            origin=jit.Service(
                position=surface.get_or_create_position([0, 0]),
                earliest=0.0,
                latest=10.0,
            ),
            destination=jit.Service(
                position=surface.get_or_create_position([1, 1]),
            ),
        )

        pickup_stop = jit.Stop(vehicle, surface.get_or_create_position([0, 0]), route.current_stop)
        delivery_stop = jit.Stop(vehicle, surface.get_or_create_position([1, 1]), pickup_stop)

        planned_trip = jit.PlannedTrip(
            vehicle=vehicle,
            trip=trip,
            pickup=pickup_stop,
            delivery=delivery_stop,
        )
        route.append_planned_trip(planned_trip)
        return route

    @classmethod
    def _build_route_2(cls, vehicle: jit.Vehicle, surface: jit.Surface) -> jit.Route:
        route = jit.Route(vehicle)

        trip = jit.Trip(
            identifier='TEST_2',
            origin=jit.Service(
                position=surface.get_or_create_position([0, 0]),
                earliest=1.0,
                latest=20.0,
            ),
            destination=jit.Service(
                position=surface.get_or_create_position([10, 10]),
            ),
        )

        pickup_stop = jit.Stop(vehicle, surface.get_or_create_position([0, 0]), route.current_stop)
        delivery_stop = jit.Stop(vehicle, surface.get_or_create_position([10, 10]), pickup_stop)

        planned_trip = jit.PlannedTrip(
            vehicle=vehicle,
            trip=trip,
            pickup=pickup_stop,
            delivery=delivery_stop,
        )
        route.append_planned_trip(planned_trip)
        return route
