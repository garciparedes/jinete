from __future__ import (
    annotations,
)

import logging
from typing import (
    TYPE_CHECKING,
)

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
    from typing import Type
    from ....models import Result
    from .iterators import InsertionIterator

logger = logging.getLogger(__name__)


class InsertionAlgorithm(Algorithm):
    def __init__(self, iterator_cls: Type[InsertionIterator] = None, initial: Result = None, **kwargs):
        super().__init__(**kwargs)
        if iterator_cls is None:
            iterator_cls = RankingInsertionIterator
        self.initial = initial
        self.iterator_cls = iterator_cls
        self.kwargs = kwargs

    def _build_iterator(self) -> InsertionIterator:
        kwargs = self.kwargs.copy()
        if self.initial is not None and "routes" not in kwargs:
            kwargs["routes"] = self.initial.routes
        return self.iterator_cls(**kwargs)

    def _optimize(self) -> Planning:
        iterator = self._build_iterator()

        for route in iterator:
            if not route.feasible:
                break
            iterator._set_route(route)

        planning = Planning(iterator._routes)
        return planning
