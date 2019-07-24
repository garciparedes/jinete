from __future__ import annotations

import logging
from abc import ABC
from dataclasses import dataclass, field
from typing import (
    TYPE_CHECKING,
)

from uuid import (
    uuid4,
)

if TYPE_CHECKING:
    from uuid import (
        UUID,
    )

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Position(ABC):
    uuid: UUID = field(default_factory=uuid4, hash=False)


@dataclass(frozen=True)
class XYPosition(Position):
    lat: float = field(default=0)
    lon: float = field(default=0)

    def __eq__(self, other: 'XYPosition') -> bool:
        return isinstance(other, XYPosition) and self.is_equal(other.lat, other.lon)

    def is_equal(self, lat, lon, *args, **kwargs):
        return self.lat == lat and self.lon == lon
