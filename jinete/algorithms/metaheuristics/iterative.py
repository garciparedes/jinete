"""Iterative algorithm class definitions."""

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
    """Iterative algorithm implementation.

    This class implements an iterative procedure to optimize a planning. It works applying a parametrized algorithm
    for a defined number of episodes. It's mostly used as a component of more complicated metaheuristics.
    """

    def __init__(self, episodes: int = 3, algorithm_cls: Type[Algorithm] = None, seed: int = 56, *args, **kwargs):
        """Construct a new instance.

        :param episodes: The number of episodes to repeat the algorithm.
        :param algorithms_cls: The sequence of algorithm classes to be applied.
        :param seed: A seed to manage randomness.
        :param args: Additional positional arguments.
        :param kwargs: Additional named arguments.
        """
        super().__init__(*args, **kwargs)
        if algorithm_cls is None:
            algorithm_cls = InsertionAlgorithm
        self.episodes = episodes
        self.algorithm_cls = algorithm_cls
        self.random = Random(seed)

        self.args = args
        self.kwargs = kwargs

    def _build_algorithm(self, *args, **kwargs) -> Algorithm:
        args = (*self.args, *args)
        kwargs.update(self.kwargs)

        return self.algorithm_cls(*args, **kwargs)

    def _optimize(self) -> Planning:
        best: Optional[Result] = None
        for i in range(self.episodes):
            seed = self.random.randint(0, MAX_INT)
            current = self._build_algorithm(seed=seed).optimize()
            best = self._objective.best(best, current)

        assert best is not None
        return best.planning
