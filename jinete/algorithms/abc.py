from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from time import time

from ..models import (
    Planning,
)

if TYPE_CHECKING:
    from ..models import (
        Fleet,
        Job,
        Route,
    )
logger = logging.getLogger(__name__)


class Algorithm(ABC):

    def __init__(self, fleet: Fleet, job: Job, *args, **kwargs):
        self.fleet = fleet
        self.job = job

    @abstractmethod
    def optimize(self) -> Planning:
        pass
