from __future__ import annotations

import logging
from typing import (
    TYPE_CHECKING,
)
from .constants import (
    MAX_FLOAT,
)
from .abc import (
    Model,
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


class Service(Model):
    __slots__ = (
        'position',
        'earliest',
        'latest',
        'duration',
    )
    position: Position
    earliest: float
    latest: float
    duration: float

    def __init__(self, position: Position, earliest: float = 0.0, latest: float = MAX_FLOAT, duration: float = 0.0):
        self.position = position
        self.earliest = earliest
        self.latest = latest
        self.duration = duration

    def __deepcopy__(self, memo: Dict[int, Any]) -> Service:
        return self

    def as_dict(self) -> Dict[str, Any]:
        return {
            'position': self.position,
            'earliest': self.earliest,
            'latest': self.latest,
            'duration': self.duration,
        }

    def distance_to(self, other: Service) -> float:
        return self.position.distance_to(other.position)

    def time_to(self, other: Service, *args, **kwargs) -> float:
        return self.position.time_to(other.position, *args, **kwargs)
