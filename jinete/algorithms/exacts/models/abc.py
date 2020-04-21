"""Abstract class definitions."""

from __future__ import (
    annotations,
)

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


class LinearModel(ABC):
    """Linear model class.

    This class contains the linear model representation of the defined problem.
    """

    def __init__(self, fleet: Fleet, job: Job, *args, **kwargs):
        """Construct a new instance.

        :param fleet: The fleet of vehicles.
        :param job: The set of trips to be completed.
        :param args: Additional positional arguments.
        :param kwargs: Additional named arguments.
        """
        self.fleet = fleet
        self.job = job

    @property
    @abstractmethod
    def _problem(self) -> lp.LpProblem:
        pass

    @property
    @abstractmethod
    def _objective(self) -> lp.LpConstraintVar:
        pass

    @property
    @abstractmethod
    def _constraints(self) -> List[lp.LpConstraint]:
        pass

    @abstractmethod
    def solve(self) -> Set[Route]:
        """Perform a optimization based on the linear model.

        :return A set of optimized routes.
        """
        pass
