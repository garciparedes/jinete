from __future__ import annotations
import logging
from abc import (
    ABC,
    abstractmethod)
from collections import defaultdict

from typing import (
    TYPE_CHECKING,
)

from uuid import (
    uuid4,
)

from .abc import (
    Model,
)
from .constants import (
    DistanceMetric,
)
from .positions import (
    GeometricPosition,
)

if TYPE_CHECKING:
    from typing import (
        Set,
        Any,
        Dict,
    )
    from uuid import (
        UUID,
    )
    from .positions import (
        Position,
    )

logger = logging.getLogger(__name__)


class Surface(Model, ABC):
    uuid: UUID
    positions: Set[Position]

    def __init__(self, positions: Set[Position] = None, uuid: UUID = None, *args, **kwargs):
        if uuid is None:
            uuid = uuid4()
        if positions is None:
            positions = set()
        self.uuid = uuid
        self.positions = positions

    def get_or_create_position(self, *args, **kwargs) -> Position:
        position = self._build_position(*args, **kwargs)
        if position not in self.positions:
            self.positions.add(position)
        return position

    @abstractmethod
    def _build_position(self, *args, **kwargs):
        pass

    @abstractmethod
    def distance(self, position_a: Position, position_b: Position) -> float:
        pass

    @abstractmethod
    def time(self, position_a: Position, position_b: Position, now: float) -> float:
        pass

    def as_dict(self) -> Dict[str, Any]:
        positions_str = ', '.join(str(position) for position in self.positions)
        dict_values = {
            'positions': f'{{{positions_str}}}'
        }
        return dict_values


class GeometricSurface(Surface):
    cached_distance: Dict[Position, Dict[Position, float]]

    def __init__(self, metric: DistanceMetric, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metric = metric

        self.cached_distance = defaultdict(dict)

    def _build_position(self, *args, **kwargs):
        return GeometricPosition(surface=self, *args, **kwargs)

    def distance(self, position_a: Position, position_b: Position) -> float:
        try:
            distance = self.cached_distance[position_a][position_b]
        except KeyError:
            distance = self.metric(position_a, position_b)
            self.cached_distance[position_a][position_b] = distance

        return distance

    def time(self, position_a: Position, position_b: Position, now: float) -> float:
        return self.distance(position_a, position_b)
