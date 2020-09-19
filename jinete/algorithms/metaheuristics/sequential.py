"""Sequential algorithm class definitions."""

from __future__ import (
    annotations,
)

import logging
from random import (
    Random,
)
from typing import (
    TYPE_CHECKING,
)

from ...models import (
    MAX_INT,
    Planning,
)
from ..abc import (
    Algorithm,
)

if TYPE_CHECKING:
    from ...models import Result
    from typing import (
        Dict,
        Any,
        Sequence,
        Tuple,
        Type,
    )

logger = logging.getLogger(__name__)


class SequentialAlgorithm(Algorithm):
    """Sequential algorithm implementation.

    This implementation is based on the application of a sequence of algorithm implementations. It's mostly used as a
    component of more complicated metaheuristics.
    """

    def __init__(
        self,
        initial: Result = None,
        algorithms_cls: Sequence[Tuple[Type[Algorithm], Dict[str, Any]]] = None,
        seed: int = 56,
        *args,
        **kwargs
    ):
        """Construct a new instance.

        :param initial: The initial result from to start the optimization process.
        :param algorithms_cls: The sequence of algorithm classes to be applied.
        :param seed: A seed to manage randomness.
        :param args: Additional positional arguments.
        :param kwargs: Additional named arguments.
        """
        super().__init__(*args, **kwargs)

        if algorithms_cls is None:
            from ..heuristics import (
                InsertionAlgorithm,
                LocalSearchAlgorithm,
                ReallocationLocalSearchStrategy,
            )

            algorithms_cls = [
                (LocalSearchAlgorithm, {**kwargs, "strategy_cls": ReallocationLocalSearchStrategy}),
                (InsertionAlgorithm, kwargs),
            ]

        self.random = Random(seed)

        self.initial = initial
        self.algorithms_cls = algorithms_cls

    def _build_algorithm(self, cls, **kwargs) -> Algorithm:
        assert issubclass(cls, Algorithm)
        kwargs = kwargs.copy()
        if "fleet" not in kwargs:
            kwargs["fleet"] = self.fleet
        if "job" not in kwargs:
            kwargs["job"] = self.job
        if "seed" not in kwargs:
            kwargs["seed"] = self.random.randint(0, MAX_INT)
        return cls(**kwargs)

    def _optimize(self) -> Planning:
        current = self.initial
        for algorithm_cls, algorithm_kwargs in self.algorithms_cls:
            current = self._build_algorithm(algorithm_cls, **algorithm_kwargs, initial=current).optimize()
        return current.planning
