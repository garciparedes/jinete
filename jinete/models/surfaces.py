from __future__ import annotations
import logging
from abc import (
    ABC,
    abstractmethod,
)
from collections import (
    defaultdict,
)

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
        Generator,
        Tuple,
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
    def time(self, position_a: Position, position_b: Position, **kwargs) -> float:
        pass

    def __iter__(self) -> Generator[Tuple[str, Any], None, None]:
        yield from (
            ('position_coordinates', tuple(position.coordinates for position in self.positions)),
        )


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
            distance = self.metric(position_a.coordinates, position_b.coordinates)
            self.cached_distance[position_a][position_b] = distance

        return distance

    def time(self, position_a: Position, position_b: Position, **kwargs) -> float:
        return self.distance(position_a, position_b)
