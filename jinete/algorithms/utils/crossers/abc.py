from __future__ import annotations

import logging
from abc import (
    ABC,
    abstractmethod,
)
from copy import deepcopy
from typing import (
    TYPE_CHECKING,
)

from ....exceptions import (
    StopPlannedTripIterationException,
)
from ....models import (
    Route,
    ShortestTimeRouteCriterion,
)

if TYPE_CHECKING:
    from typing import (
        Set,
        Optional,
        Type,
    )
    from ....models import (
        PlannedTrip,
        Vehicle,
        Fleet,
        Trip,
        Job,
        RouteCriterion,
    )

logger = logging.getLogger(__name__)


class Crosser(ABC):
    fleet: Fleet
    job: Job
    criterion_cls: Type[RouteCriterion]
    _criterion: Optional[RouteCriterion]

    def __init__(self, fleet: Fleet, job: Job, criterion_cls: Type[RouteCriterion] = None,
                 routes: Set[Route] = None, *args, **kwargs):
        if criterion_cls is None:
            criterion_cls = ShortestTimeRouteCriterion

        pending_trips = set(job.trips)
        if routes is None:
            routes = set(Route(vehicle) for vehicle in fleet.vehicles)
        else:
            routes = deepcopy(routes)
            for route in routes:
                pending_trips -= set(route.trips)

        self.fleet = fleet
        self.job = job
        self.routes_container = {
            route.vehicle: route
            for route in routes
        }
        self._pending_trips = pending_trips

        self.criterion_cls = criterion_cls
        self._criterion = None

        self.args = args
        self.kwargs = kwargs

    @property
    def routes(self) -> Set[Route]:
        return set(self.routes_container.values())

    def set_route(self, route: Route):
        old = self.routes_container[route.vehicle]
        self.routes_container[route.vehicle] = route
        for trip in set(route.trips) - set(old.trips):
            self.mark_trip_as_done(trip)
        for trip in set(old.trips) - set(route.trips):
            self.mark_trip_as_undone(trip)

    @property
    def criterion(self) -> RouteCriterion:
        if self._criterion is None:
            self._criterion = self.criterion_cls(*self.args, **self.kwargs)
        return self._criterion

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
                raise StopPlannedTripIterationException()
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
