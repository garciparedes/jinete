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
    )
    from .routes import (
        Route,
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

        self.routes = routes
        self.uuid = uuid

    def __iter__(self):
        yield from self.routes

    @property
    def loaded_routes(self):
        return set(route for route in self.routes if route.loaded)

    def as_dict(self) -> Dict[str, Any]:
        return {
            'uuid': self.uuid,
        }

    def __deepcopy__(self, memo: Dict[int, Any]) -> Planning:
        planning = Planning()
        memo[id(self)] = planning

        planning.routes = deepcopy(self.routes, memo)

        return planning
