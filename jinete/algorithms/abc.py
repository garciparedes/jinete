from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from time import time

from ..models import (
    Planning,
    Result,
)

if TYPE_CHECKING:
    from ..models import (
        Fleet,
        Job,
        Objective,
    )
logger = logging.getLogger(__name__)


class Algorithm(ABC):

    def __init__(self, fleet: Fleet, job: Job, *args, **kwargs):
        """
        The constructor of the class.

        :param fleet: The `Fleet` of available vehicles to use on the solution.
        :param job: The `Job` composed of the requested `Trip` objects to be satisfied by the solution.
        :param args: Additional positional arguments.
        :param kwargs: Additional named arguments.
        """
        self.fleet = fleet
        self.job = job

    @property
    def _objective(self) -> Objective:
        return self.job.objective

    def optimize(self) -> Result:
        """
        Performs an optimization over the ``job`` using the ``fleet`` and generates a ``Result`` object containing the
        generated results.

        :return: A ``Result`` object.
        """
        logger.info(f'Optimizing with {self.__class__.__name__}...')

        start_time = time()
        planning = self._optimize()
        end_time = time()
        computation_time = end_time - start_time

        result = Result(
            algorithm=self,
            planning=planning,
            computation_time=computation_time,
        )
        logger.info(f'Optimized with {self.__class__.__name__} obtaining {"" if result.feasible else "non "}'
                    f'feasible results!')
        return result

    @abstractmethod
    def _optimize(self) -> Planning:
        pass
