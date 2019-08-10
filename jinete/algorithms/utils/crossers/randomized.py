from __future__ import annotations

import logging
from itertools import islice
from random import Random
from typing import TYPE_CHECKING
from collections import OrderedDict
from uuid import UUID

from .ordered import (
    OrderedCrosser,
)
from .abc import (
    Crosser,
)

if TYPE_CHECKING:
    from typing import (
        Optional,
        Dict,
        Iterable,
        Set,
    )
    from ....models import (
        PlannedTrip,
        Trip,
        Route,
    )

logger = logging.getLogger(__name__)


class RandomizedCrosser(OrderedCrosser):

    def __init__(self, randomized_size: int = 3, seed: int = 56, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.randomized_size = randomized_size
        self.random = Random(seed)

    def get_planned_trip(self) -> Optional[PlannedTrip]:
        if len(self.ranking) == 0:
            return None

        candidates = list()
        for sub_ranking in self.ranking.values():
            if len(sub_ranking) == 0:
                continue
            current = next(iter(sub_ranking.values()))
            if len(candidates) == 0 or candidates[-1] < current:
                if len(candidates) != 0:
                    candidates.pop()
                candidates.append(current)
                candidates.sort()
        if len(candidates) == 0:
            return None
        best = self.random.choice(candidates)
        return best
