from __future__ import annotations

import logging
from sys import maxsize
from typing import (
    TYPE_CHECKING,
    Optional,
)

from uuid import (
    uuid4,
)

if TYPE_CHECKING:
    from uuid import (
        UUID,
    )
    from .positions import (
        Position,
    )

logger = logging.getLogger(__name__)


class Trip(object):
    identifier: str
    origin: Position
    destination: Position
    earliest: float
    timeout: Optional[float]
    on_time_bonus: float
    load_time: float
    capacity: float
    uuid: UUID

    def __init__(self, identifier: str, origin: Position, destination: Position, earliest: float = 0.0,
                 timeout: Optional[float] = None, on_time_bonus: float = 0.0, load_time: float = 0.0,
                 inbound: bool = True, capacity: float = 1, uuid: UUID = None, with_caching: bool = True):
        if uuid is None:
            uuid = uuid4()
        self.identifier = identifier
        self.origin = origin
        self.destination = destination
        self.earliest = earliest
        self.timeout = timeout
        self.on_time_bonus = on_time_bonus
        self.load_time = load_time
        self.inbound = inbound
        self.capacity = capacity
        self.uuid = uuid

        self.with_caching = with_caching
        self._distance = None
        # self._duration = dict()
        self._duration = None

    @staticmethod
    def build_empty(origin: Position, destination: Position) -> 'Trip':
        return Trip('EMPTY', origin, destination, capacity=0)

    @property
    def latest(self) -> float:
        if self.timeout is None:
            return maxsize
        return self.earliest + self.timeout

    @property
    def empty(self) -> bool:
        return self.capacity == 0

    @property
    def distance(self) -> float:
        if self._distance is None or not self.with_caching:
            self._distance = self.origin.distance_to(self.destination)
        return self._distance

    def duration(self, now: float):
        # if now not in self._duration or not self.with_caching:
        #     self._duration[now] = self.origin.time_to(self.destination, now)
        # return self._duration[now]
        if self._duration is None or not self.with_caching:
            self._duration = self.origin.time_to(self.destination, now)
        return self._duration
