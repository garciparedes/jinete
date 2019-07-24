from abc import ABC, abstractmethod
from typing import Set

from ..models import (
    Vehicle,
    Trip,
)


class Loader(ABC):

    @property
    @abstractmethod
    def fleet(self) -> Set[Vehicle]:
        pass

    @property
    @abstractmethod
    def trips(self) -> Set[Trip]:
        pass
