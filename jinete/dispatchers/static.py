from __future__ import annotations

from .abc import Dispatcher

from ..models import (
    Result,
)


class StaticDispatcher(Dispatcher):

    def run(self) -> Result:
        loader = self.loader_cls()

        job = loader.job
        fleet = loader.fleet
        algorithm = self.algorithm_cls(fleet=fleet, job=job)

        result = algorithm.optimize()

        if self.storer_cls is not None:
            storer = self.storer_cls(result=result)
            storer.store()

        return result
