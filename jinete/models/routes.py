from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import timedelta
from typing import (
    TYPE_CHECKING,
    Tuple,
)

from uuid import (
    uuid4,
)

if TYPE_CHECKING:
    from .vehicles import (
        Vehicle,
    )
    from .trips import (
        Trip,
        PlannedTrip,
    )
    from uuid import (
        UUID,
    )

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Route(object):
    planned_trips: Tuple[PlannedTrip]
    vehicle: Vehicle

    uuid: UUID = field(default_factory=uuid4)

    @property
    def feasible(self) -> bool:
        return True

    @property
    def first_planned_trip(self) -> PlannedTrip:
        return min(self.planned_trips, key=lambda pt: pt.collection_time)

    @property
    def first_trip(self) -> Trip:
        return self.first_planned_trip.trip

    @property
    def last_planned_trip(self) -> PlannedTrip:
        return max(self.planned_trips, key=lambda pt: pt.delivery_time)

    @property
    def last_trip(self) -> Trip:
        return self.last_planned_trip.trip

    @property
    def duration(self) -> timedelta:
        return self.last_planned_trip.delivery_time - self.first_planned_trip.collection_time
