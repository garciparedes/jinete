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
        self.fleet = fleet
        self.job = job

    @property
    def objective(self) -> Objective:
        return self.job.objective

    def optimize(self) -> Result:
        logger.info(f'Optimizing with {self.__class__.__name__}...')

        start_time = time()
        planning = self._optimize()
        end_time = time()
        computation_time = end_time - start_time

        result = Result(
            fleet=self.fleet,
            job=self.job,
            algorithm_cls=self.__class__,
            planning=planning,
            computation_time=computation_time,
        )
        logger.info(f'Optimized with {self.__class__.__name__}!')
        return result

    @abstractmethod
    def _optimize(self) -> Planning:
        pass
