from __future__ import annotations

import logging
from dataclasses import (
    dataclass,
    field,
)
from typing import (
    TYPE_CHECKING,
    Set,
    Optional)
from uuid import (
    uuid4,
)

if TYPE_CHECKING:
    from .routes import (
        Route,
    )
    from uuid import (
        UUID,
    )
    from .surfaces import (
        Surface,
    )

logger = logging.getLogger(__name__)


class Planning(object):
    routes: Set[Route]
    computation_time: float
    # surface: Optional[Surface]
    uuid: UUID

    def __init__(self, routes: Set[Route], uuid: UUID = None):
        if uuid is None:
            uuid = uuid4()

        self.routes = routes
        self.uuid = uuid
