"""
Contains entities to represent trips in the data model.
"""

from __future__ import (
    annotations,
)

import logging
from typing import (
    TYPE_CHECKING,
)

from cached_property import (
    cached_property,
)

from .abc import (
    Model,
)
from .constants import (
    MAX_FLOAT,
)
from .services import (
    Service,
)

if TYPE_CHECKING:
    from typing import (
        Dict,
        Any,
        Generator,
        Tuple,
    )
    from .positions import Position

logger = logging.getLogger(__name__)


class Trip(Model):
    __slots__ = (
        "identifier",
        "origin",
        "destination",
        "on_time_bonus",
        "capacity",
        "timeout",
    )
    identifier: str
    """
    The unique identifier of the trip.
    """

    origin_position: Position
    """
    The position for the pickup service.
    """

    destination_position: Position
    """
    The position for the delivery service.
    """

    origin_earliest: float
    """
    The earliest time to start the pickup service.
    """

    timeout: float
    """
    The max trip duration, from the pickup latest time to the delivery earliest time.
    """

    on_time_bonus: float
    """
    The applied bonus if the trip starts at its earliest time (need to be set up through the cost function).
    """

    origin_duration: float
    """
    The requested duration to perform the origin service.
    """

    capacity: float
    """
    The requested capacity of the trip.
    """

    def __init__(
        self,
        identifier: str,
        origin: Service,
        destination: Service,
        capacity: float = 1,
        on_time_bonus: float = 0.0,
        timeout: float = MAX_FLOAT,
    ):
        """

        :param identifier:
        :param origin:
        :param destination:
        :param capacity:
        :param on_time_bonus:
        :param timeout:
        """
        self.identifier = identifier
        self.origin = origin
        self.destination = destination
        self.on_time_bonus = on_time_bonus
        self.capacity = capacity
        self.timeout = timeout

    @property
    def origin_position(self) -> Position:
        return self.origin.position

    @property
    def origin_earliest(self) -> float:
        return max(self.destination.earliest - self.destination.duration - self.timeout, self.origin.earliest,)

    @property
    def origin_latest(self) -> float:
        return min(
            self.destination.latest - self.destination.duration - self.origin.time_to(self.destination),
            self.origin.latest,
        )

    @property
    def origin_duration(self) -> float:
        return self.origin.duration

    @property
    def destination_position(self) -> Position:
        return self.destination.position

    @cached_property
    def destination_earliest(self) -> float:
        return max(
            self.origin.earliest + self.origin.duration + self.origin.time_to(self.destination),
            self.destination.earliest,
        )

    @cached_property
    def destination_latest(self) -> float:
        return min(self.origin.latest + self.origin.duration + self.timeout, self.destination.latest,)

    @property
    def destination_duration(self) -> float:
        return self.destination.duration

    @property
    def empty(self) -> bool:
        return self.capacity == 0

    @cached_property
    def distance(self) -> float:
        return self.origin_position.distance_to(self.destination_position)

    def duration(self, now: float):
        return self.origin_position.time_to(self.destination_position, now)

    def __deepcopy__(self, memo: Dict[int, Any]) -> Trip:
        return self

    def __iter__(self) -> Generator[Tuple[str, Any], None, None]:
        yield from (
            ("identifier", self.identifier),
            ("origin", tuple(self.origin)),
            ("destination", tuple(self.destination)),
            ("on_time_bonus", self.on_time_bonus),
            ("capacity", self.capacity),
            ("timeout", self.timeout),
        )
