from __future__ import annotations

import logging
from copy import deepcopy
from typing import TYPE_CHECKING
from uuid import (
    uuid4,
)
from .abc import (
    Model,
)

if TYPE_CHECKING:
    from typing import (
        Set,
        Dict,
        Any,
        Iterator,
        Generator,
        Tuple,
    )
    from .routes import (
        Route,
    )
    from .trips import (
        Trip,
    )
    from .planned_trips import (
        PlannedTrip,
    )
    from .vehicles import (
        Vehicle,
    )
    from uuid import (
        UUID,
    )

logger = logging.getLogger(__name__)


class Planning(Model):
    routes: Set[Route]
    uuid: UUID

    def __init__(self, routes: Set[Route] = None, uuid: UUID = None):
        if uuid is None:
            uuid = uuid4()
        if routes is None:
            routes = set()

        self.routes = routes
        self.uuid = uuid

    @property
    def loaded_routes(self):
        return set(route for route in self.routes if route.loaded)

    @property
    def vehicles(self) -> Iterator[Vehicle]:
        for route in self.routes:
            yield route.vehicle

    @property
    def planned_trips(self) -> Iterator[PlannedTrip]:
        for route in self.routes:
            yield from route.planned_trips

    @property
    def trips(self) -> Iterator[Trip]:
        yield from (planned_trip.trip for planned_trip in self.planned_trips)

    def __iter__(self) -> Generator[Tuple[str, Any], None, None]:
        yield from (
            ('uuid', self.uuid),
            ('route_uuids', tuple(route.uuid for route in self.routes))
        )

    def __deepcopy__(self, memo: Dict[int, Any]) -> Planning:
        planning = Planning()
        memo[id(self)] = planning

        planning.routes = deepcopy(self.routes, memo)

        return planning
