from __future__ import annotations

import logging
from typing import TYPE_CHECKING

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from .models import (
        Route,
        Trip,
        PlannedTrip,
    )


class JineteException(Exception):

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class StopPlannedTripIterationException(JineteException):

    def __init__(self):
        message = f'There are no more Planned Trips to iterate over them.'
        super().__init__(message=message)


class NonFeasiblePlannedTripException(JineteException):

    def __init__(self, planned_trip: PlannedTrip):
        assert planned_trip.feasible is False

        self.planned_trip = planned_trip
        message = f'Planned Trip "{planned_trip}" is not feasible.'
        super().__init__(message=message)


class NonFeasibleRouteException(JineteException):

    def __init__(self, route: Route):
        assert route.feasible is False

        self.route = route
        message = f'Route "{route}" is not feasible.'
        super().__init__(message=message)
