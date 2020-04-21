"""Abstract module which defines the high level scheduling during the process of optimization."""

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

from ..storers import (
    NaiveStorer,
)

if TYPE_CHECKING:
    from typing import Type
    from ..loaders import Loader
    from ..models import Result
    from ..algorithms import Algorithm
    from ..storers import Storer


class Dispatcher(ABC):
    """Dispatch the problem instances."""

    def __init__(self, loader_cls: Type[Loader], algorithm_cls: Type[Algorithm], storer_cls: Type[Storer] = None):
        """Construct a new instance.

        :param loader_cls: Loads problem instances.
        :param algorithm_cls: Generates the solution for the problem instance.
        :param storer_cls: Stores problem instances.
        """
        if storer_cls is None:
            storer_cls = NaiveStorer
        self.loader_cls = loader_cls
        self.algorithm_cls = algorithm_cls
        self.storer_cls = storer_cls

    @abstractmethod
    def run(self) -> Result:
        """Start the execution of the dispatcher.

        :return: A result object containing the generated solution.
        """
        pass
