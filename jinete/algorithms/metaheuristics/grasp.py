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
from .sequential import (
    SequentialAlgorithm,
)
from .iterative import (
    IterativeAlgorithm,
)

if TYPE_CHECKING:
    from typing import (
        Dict,
        Any,
    )

logger = logging.getLogger(__name__)


class GraspAlgorithm(Algorithm):

    def __init__(self, no_improvement_threshold: int = 1, first_solution_kwargs: Dict[str, Any] = None,
                 local_search_kwargs: Dict[str, Any] = None,
                 seed: int = 56, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if first_solution_kwargs is None:
            first_solution_kwargs = dict()
        if local_search_kwargs is None:
            local_search_kwargs = dict()

        self.no_improvement_threshold = no_improvement_threshold
        self.first_solution_kwargs = first_solution_kwargs
        self.local_search_kwargs = local_search_kwargs
        self.random = Random(seed)

    def _build_first_solution_algorithm(self, **kwargs) -> Algorithm:
        kwargs.update(self.first_solution_kwargs.copy())
        if 'fleet' not in kwargs:
            kwargs['fleet'] = self.fleet
        if 'job' not in kwargs:
            kwargs['job'] = self.job
        if 'seed' not in kwargs:
            kwargs['seed'] = self.random.randint(0, MAX_INT)
        return IterativeAlgorithm(**kwargs)

    def _build_local_search_algorithm(self, **kwargs) -> Algorithm:
        kwargs.update(self.local_search_kwargs.copy())
        if 'fleet' not in kwargs:
            kwargs['fleet'] = self.fleet
        if 'job' not in kwargs:
            kwargs['job'] = self.job
        if 'seed' not in kwargs:
            kwargs['seed'] = self.random.randint(0, MAX_INT)
        return SequentialAlgorithm(**kwargs)

    def _optimize(self) -> Planning:
        iterative = self._build_first_solution_algorithm()
        best = iterative.optimize()

        no_improvement_count = 0
        while no_improvement_count < self.no_improvement_threshold:
            no_improvement_count += 1

            current = self._build_local_search_algorithm(initial=best).optimize()

            best = self._objective.best(best, current)

            if best == current:
                no_improvement_count = 0

        return best.planning
