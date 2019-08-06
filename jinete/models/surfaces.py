from __future__ import annotations
import logging
from abc import (
    ABC,
    abstractmethod)

from math import sqrt
from typing import (
    TYPE_CHECKING,
    Set,
    Any, Dict)

from uuid import (
    uuid4,
)

from .abc import (
    Model,
)
from .positions import (
    XYPosition,
)

if TYPE_CHECKING:
    from uuid import (
        UUID,
    )
    from .positions import (
        Position,
    )

logger = logging.getLogger(__name__)


class Surface(Model, ABC):
    uuid: UUID

    def __init__(self, positions: Set[Position] = None, uuid: UUID = None, *args, **kwargs):
        if uuid is None:
            uuid = uuid4()
        if positions is None:
            positions = set()
        self.uuid = uuid
        self.positions = positions

    def get_or_create_position(self, *args, **kwargs) -> Position:
        position = self._build_position(*args, **kwargs)
        self.positions.add(position)
        return position

    @abstractmethod
    def _build_position(self, *args, **kwargs):
        pass

    @abstractmethod
    def distance(self, position_a: Position, position_b: Position) -> float:
        pass

    def time(self, position_a: Position, position_b: Position, now: float) -> float:
        return self.distance(position_a, position_b)

    def as_dict(self) -> Dict[str, Any]:
        positions_str = ', '.join(str(position) for position in self.positions)
        dict_values = {
            'positions': f'{{{positions_str}}}'
        }
        return dict_values


class GeometricSurface(Surface):
    positions: Set[XYPosition]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _build_position(self, *args, **kwargs):
        return XYPosition(surface=self, *args, **kwargs)

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
