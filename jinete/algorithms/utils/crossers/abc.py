from __future__ import annotations

import logging
from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    TYPE_CHECKING,
)

from ....exceptions import (
    NonFeasiblePlannedTripFoundException,
)
from ....models import (
    Route,
)

if TYPE_CHECKING:
    from typing import (
        Set,
        Optional,
    )
    from ....models import (
        PlannedTrip,
        Vehicle,
        Fleet,
        Trip,
        Job,
    )

logger = logging.getLogger(__name__)


class Crosser(ABC):

    def __init__(self, fleet: Fleet, job: Job):
        self.fleet = fleet
        self.job = job
        self.routes = set(Route(vehicle) for vehicle in self.vehicles)
        self._pending_trips = set(self.trips)

    @property
    def vehicles(self) -> Set[Vehicle]:
        return self.fleet.vehicles

    @property
    def trips(self) -> Set[Trip]:
        return self.job.trips

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            planned_trip = self.get_planned_trip()
            if planned_trip is None:
                raise NonFeasiblePlannedTripFoundException('Remaining Planned Trips are not feasible.')
            logger.debug(f'Yielding {planned_trip}...')
            return planned_trip

    @abstractmethod
    def get_planned_trip(self) -> Optional[PlannedTrip]:
        pass

    def mark_planned_trip_as_done(self, planned_trip: PlannedTrip) -> None:
        self.mark_trip_as_done(planned_trip.trip)

    def mark_trip_as_done(self, trip: Trip) -> None:
        self._pending_trips.remove(trip)

    def mark_planned_trip_as_undone(self, planned_trip: PlannedTrip) -> None:
        self.mark_trip_as_undone(planned_trip.trip)

    def mark_trip_as_undone(self, trip: Trip) -> None:
        self._pending_trips.add(trip)

    @property
    def pending_trips(self) -> Set[Trip]:
        return self._pending_trips

    @property
    def done_trips(self) -> Set[Trip]:
        return self.trips - self.pending_trips

    @property
    def completed(self) -> bool:
        return len(self.pending_trips) == 0
