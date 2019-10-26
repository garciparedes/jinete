from __future__ import annotations

from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    TYPE_CHECKING,
)

import pulp as lp

if TYPE_CHECKING:
    from typing import (
        List,
        Set,
    )
    from ....models import (
        Fleet,
        Job,
        Route,
    )


class Model(ABC):

    def __init__(self, fleet: Fleet, job: Job, *args, **kwargs):
        self.fleet = fleet
        self.job = job

    @property
    @abstractmethod
    def problem(self) -> lp.LpProblem:
        pass

    @property
    @abstractmethod
    def objective(self) -> lp.LpConstraintVar:
        pass

    @property
    @abstractmethod
    def constraints(self) -> List[lp.LpConstraint]:
        pass

    @abstractmethod
    def solve(self) -> Set[Route]:
        pass
