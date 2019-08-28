from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ...exceptions import (
    NonFeasiblePlannedTripFoundException,
)
from ...models import (
    Planning,
)
from ..abc import (
    Algorithm,
)

if TYPE_CHECKING:
    from typing import (
        Set,
    )
    from ...models import (
        Result,
        Route,
    )

logger = logging.getLogger(__name__)


class LocalSearchAlgorithm(Algorithm):

    def __init__(self, initial: Result, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial = initial
        self.args = args
        self.kwargs = kwargs

    @property
    def initial_planning(self) -> Planning:
        return self.initial.planning

    @property
    def initial_routes(self) -> Set[Route]:
        return self.initial_planning.routes

    def _optimize(self) -> Planning:
        raise NotImplementedError
