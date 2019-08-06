from __future__ import annotations

import logging
from typing import TYPE_CHECKING

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from .models import (
        Route,
        Trip,
    )


class JineteException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class PlannedTripNotFeasibleException(JineteException):

    def __init__(self, route: Route, trip: Trip):
        self.route = route
        self.trip = trip
        message = f'The {trip} is not feasible at the end of {route}.'
        super().__init__(message=message)
