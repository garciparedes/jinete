from __future__ import annotations

import logging
from typing import (
    TYPE_CHECKING,
    Optional,
)
from .constants import (
    MAX_FLOAT,
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
        'origin_earliest',
        'origin_latest',
        'destination_earliest',
        'destination_latest',
        'on_time_bonus',
        'load_capacity',
        'load_time',
        'capacity',
    )
    identifier: str
    origin: Position
    destination: Position
    origin_earliest: float
    timeout: Optional[float]
    on_time_bonus: float
    load_time: float
    capacity: float

    def __init__(self, identifier: str, origin: Position, destination: Position, origin_earliest: float = 0.0,
                 origin_latest: float = MAX_FLOAT, on_time_bonus: float = 0.0, load_time: float = 0.0,
                 capacity: float = 1, destination_earliest: float = 0.0, destination_latest: float = MAX_FLOAT):
        self.identifier = identifier
        self.origin = origin
        self.origin_earliest = origin_earliest
        self.origin_latest = origin_latest

        self.destination = destination
        self.destination_earliest = destination_earliest
        self.destination_latest = destination_latest

        self.on_time_bonus = on_time_bonus
        self.load_time = load_time
        self.capacity = capacity

    @property
    def empty(self) -> bool:
        return self.capacity == 0

    @property
    def distance(self) -> float:
        return self.origin.distance_to(self.destination)

    def duration(self, now: float):
        return self.origin.time_to(self.destination, now)

    def __deepcopy__(self, memo: Dict[int, Any]) -> Trip:
        return self
