from abc import ABC, abstractmethod
from typing import Set

from ..models import (
    Planning,
    Trip,
    Vehicle,
)


class Algorithm(ABC):

    def __init__(self, vehicles: Set[Vehicle], trips: Set[Trip], *args, **kwargs):
        self.trips = trips
        self.vehicles = vehicles

    @abstractmethod
    def optimize(self) -> Planning:
        pass
