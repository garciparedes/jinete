from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ....models import (
    Planning,
)
from ...abc import (
    Algorithm,
)
from .strategies import (
    ReallocationLocalSearchStrategy,
)

if TYPE_CHECKING:
    from typing import (
        Set,
    )
    from ....models import (
        Result,
        Route,
    )

logger = logging.getLogger(__name__)


class LocalSearchAlgorithm(Algorithm):

    def __init__(self, initial: Result, no_improvement_threshold: int = 1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial = initial
        self.args = args
        self.kwargs = kwargs
        self.strategy_cls = ReallocationLocalSearchStrategy
        self.no_improvement_threshold = no_improvement_threshold

    @property
    def initial_planning(self) -> Planning:
        return self.initial.planning

    @property
    def initial_routes(self) -> Set[Route]:
        return self.initial_planning.routes

    def _optimize(self) -> Planning:
        best = self.initial

        no_improvement_count = 0
        while no_improvement_count < self.no_improvement_threshold:
            no_improvement_count += 1

            current = self.strategy_cls(best).improve()
            best = self.objective.best(best, current)

            if best == current:
                no_improvement_count = 0

        assert best is not None

        return best.planning
