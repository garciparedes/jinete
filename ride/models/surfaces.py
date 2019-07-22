from __future__ import annotations
import logging
from abc import (
    ABC,
)
from dataclasses import (
    dataclass,
    field,
)
from math import sqrt
from typing import (
    TYPE_CHECKING,
    Set,
)

from uuid import (
    uuid4,
)

if TYPE_CHECKING:
    from uuid import (
        UUID,
    )
    from .positions import (
        XYPosition,
    )

logger = logging.getLogger(__name__)


@dataclass
class Surface(ABC):
    uuid: UUID = field(default_factory=uuid4)


@dataclass
class GeometricSurface(Surface):
    positions: Set[XYPosition] = field(default=set)

    def distance(self, position_a: XYPosition, position_b: XYPosition, auto_add: bool = False) -> float:
        if position_a not in self.positions:
            logger.warning(f'"position_a"="{position_a}" is not on "self.positions".')
            if auto_add:
                self.positions.add(position_a)

        if position_b not in self.positions:
            logger.warning(f'"position_b"="{position_b}" is not on "self.positions".')
            if auto_add:
                self.positions.add(position_b)
        return sqrt(pow(position_a.lat - position_b.lat, 2) + pow(position_a.lon - position_b.lon, 2))
