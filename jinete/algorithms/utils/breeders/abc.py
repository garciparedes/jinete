from __future__ import annotations

from abc import (
    ABC,
    abstractmethod,
)
from copy import deepcopy

from ....models import (
    Planning,
    Result,
    Objective,
)


class Breeder(ABC):

    def __init__(self, result: Result, with_copy: bool = True):
        if with_copy:
            result = deepcopy(result)

        self.result = result

    @property
    def objective(self) -> Objective:
        return self.result.objective

    @property
    def planning(self) -> Planning:
        return self.result.planning

    @abstractmethod
    def improve(self) -> Result:
        pass
