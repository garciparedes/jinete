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
from ...utils import doc_inherit

if TYPE_CHECKING:
    from ...models import (
        Result,
    )
    from typing import (
        Dict,
        Any,
        Sequence,
        Tuple,
        Type,
    )

logger = logging.getLogger(__name__)


class SequentialAlgorithm(Algorithm):

    @doc_inherit
    def __init__(self, initial: Result, algorithms_cls: Sequence[Tuple[Type[Algorithm], Dict[str, Any]]] = None,
                 seed: int = 56, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if algorithms_cls is None:
            from .iterative import IterativeAlgorithm
            from ..heuristics import (
                LocalSearchAlgorithm,
                ReallocationLocalSearchStrategy,
            )
            algorithms_cls = [
                (LocalSearchAlgorithm, {**kwargs, 'strategy_cls': ReallocationLocalSearchStrategy}),
                (IterativeAlgorithm, kwargs),
            ]

        self.random = Random(seed)

        self.initial = initial
        self.algorithms_cls = algorithms_cls

    def _build_algorithm(self, cls, **kwargs) -> Algorithm:
        assert issubclass(cls, Algorithm)
        kwargs = kwargs.copy()
        if 'fleet' not in kwargs:
            kwargs['fleet'] = self.fleet
        if 'job' not in kwargs:
            kwargs['job'] = self.job
        if 'seed' not in kwargs:
            kwargs['seed'] = self.random.randint(0, MAX_INT)
        return cls(**kwargs)

    def _optimize(self) -> Planning:
        current = self.initial
        for algorithm_cls, algorithm_kwargs in self.algorithms_cls:
            current = self._build_algorithm(algorithm_cls, **algorithm_kwargs, initial=current).optimize()
        return current.planning
