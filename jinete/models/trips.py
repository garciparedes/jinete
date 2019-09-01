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
        'earliest',
        'timeout',
        'on_time_bonus',
        'load_capacity',
        'load_time',
        'inbound',
        'capacity',
    )
    identifier: str
    origin: Position
    destination: Position
    earliest: float
    timeout: Optional[float]
    on_time_bonus: float
    load_time: float
    capacity: float

    def __init__(self, identifier: str, origin: Position, destination: Position, earliest: float = 0.0,
                 timeout: Optional[float] = None, on_time_bonus: float = 0.0, load_time: float = 0.0,
                 inbound: bool = True, capacity: float = 1):
        self.identifier = identifier
        self.origin = origin
        self.destination = destination
        self.earliest = earliest
        self.timeout = timeout
        self.on_time_bonus = on_time_bonus
        self.load_time = load_time
        self.inbound = inbound
        self.capacity = capacity

    @property
    def latest(self) -> float:
        if self.timeout is None:
            return MAX_FLOAT
        return self.earliest + self.timeout

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
