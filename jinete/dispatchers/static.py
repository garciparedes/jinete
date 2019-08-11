from time import time

from .abc import Dispatcher

from ..models import (
    Result,
)


class StaticDispatcher(Dispatcher):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self) -> Result:
        loader = self.loader_cls()

        job = loader.job
        fleet = loader.fleet
        algorithm = self.algorithm_cls(fleet=fleet, job=job)

        result = algorithm.optimize()

        storer = self.storer_cls(result=result)
        storer.store()
        return result
