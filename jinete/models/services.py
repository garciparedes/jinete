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
from uuid import (
    uuid4,
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


class Service(Model):
    __slots__ = (
        'position',
        'earliest',
        'latest',
        'duration',
        'identifier',
    )
    position: Position
    earliest: float
    latest: float
    duration: float
    identifier: str

    def __init__(
        self,
        position: Position,
        earliest: float = 0.0,
        latest: float = MAX_FLOAT,
        duration: float = 0.0,
        identifier: str = None
    ):
        self.position = position
        self.earliest = earliest
        self.latest = latest
        self.duration = duration
        if identifier is None:
            identifier = str(uuid4())
        self.identifier = identifier

    def __deepcopy__(self, memo: Dict[int, Any]) -> Service:
        return self

    def __eq__(self, other: Service) -> bool:
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(tuple(self))

    def __iter__(self) -> Generator[Tuple[str, Any], None, None]:
        yield from (
            ('position', self.position),
            ('earliest', self.earliest),
            ('latest', self.latest),
            ('duration', self.duration),
            ('identifier', self.identifier),
        )

    def distance_to(self, other: Service) -> float:
        return self.position.distance_to(other.position)

    def time_to(self, other: Service, *args, **kwargs) -> float:
        return self.position.time_to(other.position, *args, **kwargs)
