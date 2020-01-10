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
    LocalSearchAlgorithm,
)
from .iterative import (
    IterativeAlgorithm,
)

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


class GraspAlgorithm(Algorithm):

    def __init__(self, first_solution_episodes: int = 1, no_improvement_threshold: int = 10,
                 seed: int = 56, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.first_solution_episodes = first_solution_episodes
        self.no_improvement_threshold = no_improvement_threshold
        self.random = Random(seed)

        self.args = args
        self.kwargs = kwargs

    def build_first_solution_algorithm(self, *args, **kwargs) -> Algorithm:
        args = (*self.args, *args)
        kwargs.update(self.kwargs)

        kwargs['episodes'] = self.first_solution_episodes
        kwargs['seed'] = self.random.randint(0, MAX_INT)

        return IterativeAlgorithm(*args, **kwargs)

    def build_local_search_algorithm(self, *args, **kwargs) -> Algorithm:
        args = (*self.args, *args)
        kwargs.update(self.kwargs)

        kwargs['seed'] = self.random.randint(0, MAX_INT),

        return LocalSearchAlgorithm(*args, **kwargs)

    def _optimize(self) -> Planning:
        iterative = self.build_first_solution_algorithm()
        best = iterative.optimize()

        no_improvement_count = 0
        while no_improvement_count < self.no_improvement_threshold:
            no_improvement_count += 1

            current = self.build_local_search_algorithm(initial=best).optimize()
            current = self.build_first_solution_algorithm(routes=current.routes).optimize()
            best = self.objective.best(best, current)

            if best == current:
                no_improvement_count = 0

        return best.planning
