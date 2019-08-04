from .abc import Dispatcher


class StaticDispatcher(Dispatcher):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        loader = self.loader_cls()

        job = loader.job
        fleet = loader.fleet

        algorithm = self.algorithm_cls(fleet=fleet, job=job)
        planning = algorithm.optimize()

        storer = self.storer_cls(planning=planning)
        storer.store()
