from __future__ import annotations

import logging
from random import Random
from typing import TYPE_CHECKING

from ...models import (
    Planning,
    MAX_INT,
)
from ..abc import (
    Algorithm,
)
from ..heuristics import (
    InsertionAlgorithm,
)

if TYPE_CHECKING:
    from typing import (
        Type,
        Optional,
    )
    from ...models import (
        Result,
    )

logger = logging.getLogger(__name__)


class IterativeAlgorithm(Algorithm):

    def __init__(self, episodes: int = 100, algorithm_cls: Type[Algorithm] = None, seed: int = 56, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if algorithm_cls is None:
            algorithm_cls = InsertionAlgorithm
        self.episodes = episodes
        self.algorithm_cls = algorithm_cls
        self.random = Random(seed)

        self.args = args
        self.kwargs = kwargs

    def build_algorithm(self, *args, **kwargs) -> Algorithm:
        args = (*self.args, *args)
        kwargs.update(self.kwargs)

        return self.algorithm_cls(*args, **kwargs)

    def _optimize(self) -> Planning:
        best: Optional[Result] = None
        for i in range(self.episodes):
            seed = self.random.randint(0, MAX_INT)
            current = self.build_algorithm(seed=seed).optimize()
            best = self.objective.best(best, current)

        assert best is not None
        return best.planning
