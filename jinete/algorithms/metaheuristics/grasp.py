"""GRASP-based algorithm class definitions."""

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
    Planning,
)
from ..abc import (
    Algorithm,
)
from .iterative import (
    IterativeAlgorithm,
)
from .sequential import (
    SequentialAlgorithm,
)

if TYPE_CHECKING:
    from typing import (
        Dict,
        Any,
        Tuple,
        Type,
    )

logger = logging.getLogger(__name__)


class GraspAlgorithm(Algorithm):
    """GRASP algorithm implementation.

    This implementation is based on the Greedy Randomized Adaptive Search Procedure meta-heuristic. For more information
    about how it works, you can visit the following link:
    https://en.wikipedia.org/wiki/Greedy_randomized_adaptive_search_procedure
    """

    def __init__(
        self,
        no_improvement_threshold: int = 1,
        first_solution_kwargs: Dict[str, Any] = None,
        local_search_kwargs: Dict[str, Any] = None,
        seed: int = 56,
        *args,
        **kwargs
    ):
        """Construct a new instance.

        :param no_improvement_threshold: Manages the number of allowed iterations without any improvement.
        :param first_solution_kwargs: Named arguments for the first solution algorithm.
        :param local_search_kwargs: Named arguments for the local search algorithm.
        :param seed: A seed to manage randomness.
        :param args: Additional positional arguments.
        :param kwargs: Additional named arguments.
        """
        super().__init__(*args, **kwargs)

        if first_solution_kwargs is None:
            first_solution_kwargs = dict()
        if local_search_kwargs is None:
            local_search_kwargs = dict()

        self.no_improvement_threshold = no_improvement_threshold
        self.first_solution_kwargs = first_solution_kwargs
        self.local_search_kwargs = local_search_kwargs
        self.random = Random(seed)
        self.args = args
        self.kwargs = kwargs

    def _build_first_solution_algorithm(self, **kwargs) -> Tuple[Type[Algorithm], Dict]:
        kwargs.update(self.first_solution_kwargs.copy())
        if "fleet" not in kwargs:
            kwargs["fleet"] = self.fleet
        if "job" not in kwargs:
            kwargs["job"] = self.job
        return IterativeAlgorithm, kwargs

    def _build_local_search_algorithm(self, **kwargs) -> Tuple[Type[Algorithm], Dict]:
        kwargs.update(self.local_search_kwargs.copy())
        if "fleet" not in kwargs:
            kwargs["fleet"] = self.fleet
        if "job" not in kwargs:
            kwargs["job"] = self.job
        kwargs["algorithm_cls"] = SequentialAlgorithm
        kwargs["restart_mode"] = False
        kwargs["episodes"] = 3
        return IterativeAlgorithm, kwargs

    def _optimize(self) -> Planning:
        algorithm = IterativeAlgorithm(
            algorithm_cls=SequentialAlgorithm,
            algorithms_cls=[self._build_first_solution_algorithm(), self._build_local_search_algorithm()],
            *self.args,
            **self.kwargs
        )
        result = algorithm.optimize()
        return result.planning
