from __future__ import annotations

import logging
from random import Random
from sys import maxsize
from typing import TYPE_CHECKING

from ...models import (
    Planning,
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
    )

logger = logging.getLogger(__name__)


class GraspAlgorithm(Algorithm):

    def __init__(self, episodes: int = 100, algorithm_cls: Type[Algorithm] = None, seed: int = 56, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if algorithm_cls is None:
            algorithm_cls = InsertionAlgorithm
        self.episodes = episodes
        self.algorithm_cls = algorithm_cls
        self.random = Random(seed)

    def build_algorithm(self, *args, **kwargs) -> Algorithm:
        return self.algorithm_cls(fleet=self.fleet, job=self.job, *args, **kwargs)

    def optimize(self) -> Planning:
        logger.info('Optimizing...')

        best = None
        for i in range(self.episodes):
            seed = self.random.randint(0, maxsize)
            current = self.build_algorithm(seed=seed).optimize()
            if best is None or best < current:
                best = current
        logger.info('Optimized!')
        return best
