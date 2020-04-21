"""High level static scheduling during the process of optimization (feeding with new trips, updating state, etc.)."""

from __future__ import (
    annotations,
)

from ..models import (
    Result,
)
from .abc import (
    Dispatcher,
)


class StaticDispatcher(Dispatcher):
    """Dispatch the problem instances in a sequential way, that is: loader -> algorithm -> storer."""

    def run(self) -> Result:
        """Start the execution of the dispatcher.

        :return: A result object containing the generated solution.
        """
        loader = self.loader_cls()

        job = loader.job
        fleet = loader.fleet
        algorithm = self.algorithm_cls(fleet=fleet, job=job)

        result = algorithm.optimize()

        if self.storer_cls is not None:
            storer = self.storer_cls(result=result)
            storer.store()

        return result
