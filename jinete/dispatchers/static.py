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

        start_time = time()
        planning = algorithm.optimize()
        end_time = time()
        computation_time = end_time - start_time

        result = Result(
            fleet=fleet,
            job=job,
            algorithm_cls=self.algorithm_cls,
            planning=planning,
            computation_time=computation_time,
        )

        storer = self.storer_cls(result=result)
        storer.store()
        return result
