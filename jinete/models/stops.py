from __future__ import annotations

import logging
from enum import (
    Enum,
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

if TYPE_CHECKING:
    from uuid import (
        UUID,
    )
    from typing import (
        Dict,
        Any,
        Set,
        Iterable,
    )
    from .positions import (
        Position,
    )
    from .planned_trips import (
        PlannedTrip
    )
    from .routes import (
        Route,
    )
    from .vehicles import (
        Vehicle,
    )

logger = logging.getLogger(__name__)


class StopKind(Enum):
    PICKUP = 1
    DELIVERY = 2

    def __str__(self):
        return self.name


class StopCause(Model):
    uuid: UUID
    planned_trip: PlannedTrip
    kind: StopKind
    stop: Stop

    def __init__(self, planned_trip: PlannedTrip, kind: StopKind, stop: Stop = None):
        self.uuid = uuid4()
        self.planned_trip = planned_trip
        self.kind = kind
        self.stop = stop

    @property
    def planned_trip_uuid(self):
        return self.planned_trip.uuid

    def as_dict(self) -> Dict[str, Any]:
        return {
            'uuid': self.uuid,
            'planned_trip_uuid': self.planned_trip_uuid,
            'kind': self.kind
        }


class Stop(Model):
    uuid: UUID
    route: Route
    position: Position

    def __init__(self, route: Route, position: Position, previous: Stop, following: Stop = None,
                 changes: Iterable[StopCause] = None):
        if changes is None:
            changes = tuple()
        self.uuid = uuid4()
        self.route = route
        self.position = position
        self.causes = set(changes)

        self.previous = previous
        self.following = following

    def append_stop_cause(self, stop_cause: StopCause) -> None:
        stop_cause.stop = self
        self.causes.add(stop_cause)

    def as_dict(self) -> Dict[str, Any]:
        return {
            'uuid': self.uuid,
            'position': self.position,
        }

    @property
    def vehicle(self) -> Vehicle:
        return self.route.vehicle

    @property
    def previous_time(self) -> float:
        if self.previous is None:
            return self.vehicle.earliest
        return self.previous.time

    @property
    def previous_position(self) -> Position:
        if self.previous is None:
            return self.vehicle.initial
        return self.previous.position

    @property
    def time(self) -> float:
        if len(self.causes) == 0:
            return 0.0
        previous_time = self.previous_time
        return previous_time + self.previous_position.time_to(self.position, previous_time)

    @property
    def planned_trips(self) -> Set[PlannedTrip]:
        return set(cause.planned_trip for cause in self.causes)
