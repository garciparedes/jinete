from __future__ import annotations

import logging
from typing import (
    TYPE_CHECKING,
    Optional,
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
    )
    from .positions import (
        Position,
    )

logger = logging.getLogger(__name__)


class Trip(object):
    __slots__ = (
        'identifier',
        'origin',
        'destination',
        'on_time_bonus',
        'capacity',
    )
    identifier: str
    origin_position: Position
    destination_position: Position
    origin_earliest: float
    timeout: Optional[float]
    on_time_bonus: float
    origin_duration: float
    capacity: float

    def __init__(self, identifier: str, origin_position: Position, destination_position: Position,
                 origin_earliest: float = 0.0, origin_latest: float = MAX_FLOAT, on_time_bonus: float = 0.0,
                 origin_duration: float = 0.0, capacity: float = 1, destination_earliest: float = 0.0,
                 destination_latest: float = MAX_FLOAT, destination_duration: float = 0.0):
        self.identifier = identifier
        self.origin = Service(
            position=origin_position,
            earliest=origin_earliest,
            latest=origin_latest,
            duration=origin_duration,
        )
        self.destination = Service(
            position=destination_position,
            earliest=destination_earliest,
            latest=destination_latest,
            duration=destination_duration,
        )
        self.on_time_bonus = on_time_bonus
        self.capacity = capacity

    @property
    def origin_position(self) -> Position:
        return self.origin.position

    @property
    def origin_earliest(self) -> float:
        return self.origin.earliest

    @property
    def origin_latest(self) -> float:
        return self.origin.latest

    @property
    def origin_duration(self) -> float:
        return self.origin.duration

    @property
    def destination_position(self) -> Position:
        return self.destination.position

    @property
    def destination_earliest(self) -> float:
        return self.destination.earliest

    @property
    def destination_latest(self) -> float:
        return self.destination.latest

    @property
    def destination_duration(self) -> float:
        return self.destination.duration

    @property
    def empty(self) -> bool:
        return self.capacity == 0

    @property
    def distance(self) -> float:
        return self.origin_position.distance_to(self.destination_position)

    def duration(self, now: float):
        return self.origin_position.time_to(self.destination_position, now)

    def __deepcopy__(self, memo: Dict[int, Any]) -> Trip:
        return self
