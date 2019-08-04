from abc import ABC, abstractmethod

from ..models import (
    Planning,
    Fleet,
    Job,
)


class Algorithm(ABC):

    def __init__(self, fleet: Fleet, job: Job, *args, **kwargs):
        self.fleet = fleet
        self.job = job

    @abstractmethod
    def optimize(self) -> Planning:
        pass
