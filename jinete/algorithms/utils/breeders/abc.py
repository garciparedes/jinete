from __future__ import annotations

from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    TYPE_CHECKING,
)
from copy import deepcopy

if TYPE_CHECKING:
    from typing import (
        Set,
    )
    from ....models import (
        Planning,
        Result,
        Objective,
        Route
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

    @property
    def routes(self) -> Set[Route]:
        return self.planning.routes

    @abstractmethod
    def improve(self) -> Result:
        pass
