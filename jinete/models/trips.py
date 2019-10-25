from __future__ import annotations

import logging
from typing import (
    TYPE_CHECKING,
)
from .abc import (
    Model,
)
from .services import (
    Service,
)
from .constants import (
    MAX_FLOAT,
)

if TYPE_CHECKING:
    from typing import (
        Dict,
        Any,
        Generator,
        Tuple,
    )
    from .positions import (
        Position,
    )

logger = logging.getLogger(__name__)


class Trip(Model):
    __slots__ = (
        'identifier',
        'origin',
        'destination',
        'on_time_bonus',
        'capacity',
        'timeout',
    )
    identifier: str
    origin_position: Position
    destination_position: Position
    origin_earliest: float
    timeout: float
    on_time_bonus: float
    origin_duration: float
    capacity: float

    def __init__(self, identifier: str, origin: Service, destination: Service, capacity: float = 1,
                 on_time_bonus: float = 0.0, timeout: float = MAX_FLOAT):
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

    def __iter__(self) -> Generator[Tuple[str, Any], None, None]:
        yield from (
            ('identifier', self.identifier),
            ('origin', tuple(self.origin)),
            ('destination', tuple(self.destination)),
            ('on_time_bonus', self.on_time_bonus),
            ('capacity', self.capacity),
            ('timeout', self.timeout),
        )
