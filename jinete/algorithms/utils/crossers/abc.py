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
from cached_property import (
    cached_property,
)

from ....exceptions import (
    StopPlannedTripIterationException,
)
from ....models import (
    Route,
    ShortestTimeRouteCriterion,
)
from ..conjecturer import (
    Conjecturer,
)

if TYPE_CHECKING:
    from typing import (
        Set,
        Optional,
        Type,
        Dict,
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
    routes_container: Dict[Vehicle, Route]

    def __init__(self, fleet: Fleet, job: Job, conjecturer_cls: Type[Conjecturer] = None,
                 criterion_cls: Type[RouteCriterion] = None, routes: Set[Route] = None, *args, **kwargs):
        if conjecturer_cls is None:
            conjecturer_cls = Conjecturer
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
        self._attractive_routes = None
        self.pending_trips = pending_trips

        self.conjecturer_cls = conjecturer_cls
        self.criterion_cls = criterion_cls

        self.args = args
        self.kwargs = kwargs

    @property
    def routes(self) -> Set[Route]:
        return set(self.routes_container.values())

    @property
    def attractive_routes(self) -> Set[Route]:
        if self._attractive_routes is None:
            self._attractive_routes = set(route for route in self.routes if any(route.planned_trips))

        if not any(any(route.planned_trips) for route in self._attractive_routes):
            empty_route = next((route for route in self.routes if not any(route.planned_trips)), None)
            if empty_route is not None:
                self._attractive_routes.add(empty_route)
        return self._attractive_routes

    def set_route(self, route: Route) -> None:
        vehicle = route.vehicle
        logger.debug(f'Updating route for vehicle with "{vehicle.identifier}" identifier...')
        old_trips = set(self.routes_container[vehicle].trips)
        self.routes_container[vehicle] = route
        for planned_trip in route.planned_trips:
            if planned_trip.trip in old_trips:
                continue
            self.mark_planned_trip_as_done(planned_trip)

    @cached_property
    def conjecturer(self) -> Conjecturer:
        return self.conjecturer_cls(*self.args, **self.kwargs)

    @cached_property
    def criterion(self) -> RouteCriterion:
        return self.criterion_cls(*self.args, **self.kwargs)

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
        logger.info(f'Marking trip with "{planned_trip.trip_identifier}" identifier as done '
                    f'over vehicle with "{planned_trip.vehicle_identifier}" identifier...')
        self.mark_trip_as_done(planned_trip.trip)

    def mark_trip_as_done(self, trip: Trip) -> None:
        logger.debug(f'Marked trip with "{trip.identifier}" identifier as done.')
        self.pending_trips.remove(trip)

    def mark_planned_trip_as_undone(self, planned_trip: PlannedTrip) -> None:
        self.mark_trip_as_undone(planned_trip.trip)

    def mark_trip_as_undone(self, trip: Trip) -> None:
        logger.debug(f'Marked trip with "{trip.identifier}" identifier as undone.')
        self.pending_trips.add(trip)

    @property
    def done_trips(self) -> Set[Trip]:
        return self.trips - self.pending_trips

    @property
    def completed(self) -> bool:
        return len(self.pending_trips) == 0
