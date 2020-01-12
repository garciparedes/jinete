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
    RankingCrosser,
)

if TYPE_CHECKING:
    from typing import (
        Type,
    )
    from .strategies import (
        Crosser,
    )

logger = logging.getLogger(__name__)


class InsertionAlgorithm(Algorithm):

    def __init__(self, crosser_cls: Type[Crosser] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if crosser_cls is None:
            crosser_cls = RankingCrosser
        self.crosser_cls = crosser_cls
        self.args = args
        self.kwargs = kwargs

    def build_crosser(self) -> Crosser:
        return self.crosser_cls(*self.args, **self.kwargs)

    def _optimize(self) -> Planning:
        crosser = self.build_crosser()

        for route in crosser:
            crosser.set_route(route)

        planning = Planning(crosser.routes)
        return planning
