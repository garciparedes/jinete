from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ....models import (
    Planning,
)
from ...abc import (
    Algorithm,
)
from .iterators import (
    RankingInsertionIterator,
)

if TYPE_CHECKING:
    from typing import (
        Type,
    )
    from .iterators import (
        InsertionIterator,
    )

logger = logging.getLogger(__name__)


class InsertionAlgorithm(Algorithm):

    def __init__(self, iterator_cls: Type[InsertionIterator] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if iterator_cls is None:
            iterator_cls = RankingInsertionIterator
        self.iterator_cls = iterator_cls
        self.args = args
        self.kwargs = kwargs

    def build_iterator(self) -> InsertionIterator:
        return self.iterator_cls(*self.args, **self.kwargs)

    def _optimize(self) -> Planning:
        iterator = self.build_iterator()

        for route in iterator:
            if not route.feasible:
                break
            iterator.set_route(route)

        planning = Planning(iterator.routes)
        return planning
