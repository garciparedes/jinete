"""Defines the hierarchy of exceptions raised and used by `jinete`'s module."""

from __future__ import (
    annotations,
)

import logging
from typing import (
    TYPE_CHECKING,
)

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from .models import (
        Route,
        Stop,
        PlannedTrip,
    )


class JineteException(Exception):
    """The base exception on `jinete`'s package."""

    def __init__(self, message: str):
        """Construct a new instance.

        :param message: A brief description of the cause.
        """
        super().__init__(message)
        self.message = message


class PreviousStopNotInRouteException(JineteException):
    """Represents an exception raised while the previous stop is not present in the target route."""

    def __init__(self, route: Route, stop: Stop):
        """Construct a new instance.

        :param route: The route without the previous stop.
        :param stop: The stop that contains the non present previous stop.
        """
        self.route = route
        self.stop = stop
        message = f'Stop "{stop}" has no previous "{stop.previous}" on the belonging route "{route}".'
        super().__init__(message=message)


class NonFeasiblePlannedTripException(JineteException):
    """Represents an exception raised while providing a non feasible route."""

    def __init__(self, planned_trip: PlannedTrip):
        """Construct a new instance.

        :param planned_trip: The non feasible planned trip.
        """
        assert planned_trip.feasible is False

        self.planned_trip = planned_trip
        message = f'Planned Trip "{planned_trip}" is not feasible.'
        super().__init__(message=message)


class NonFeasibleRouteException(JineteException):
    """Represents an exception raised while providing a non feasible route."""

    def __init__(self, route: Route):
        """Construct a new instance.

        :param route: The non feasible route.
        """
        assert route.feasible is False

        self.route = route
        message = f'Route "{route}" is not feasible.'
        super().__init__(message=message)
