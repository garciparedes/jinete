"""A set of implementations to ease the launching process on external systems."""

from __future__ import (
    annotations,
)

from typing import (
    TYPE_CHECKING,
)

from .algorithms import (
    InsertionAlgorithm,
)
from .dispatchers import (
    StaticDispatcher,
)
from .loaders import (
    FileLoader,
)
from .storers import (
    PromptStorer,
)

if TYPE_CHECKING:
    from typing import (
        Type,
        Union,
        Dict,
        Any,
    )
    from .loaders import Loader
    from .algorithms import Algorithm
    from .models import Result
    from .storers import Storer
    from .dispatchers import Dispatcher


class Solver(object):
    """Solve a problem instance in an easy way.

    This class acts as the main library's interface of use, allowing to configure all the needed classes and
    entities to generate solutions for a problem instance and providing the requested solution.
    """

    def __init__(
        self,
        algorithm: Union[str, Type[Algorithm]] = InsertionAlgorithm,
        algorithm_kwargs: Dict[str, Any] = None,
        loader: Union[str, Type[Loader]] = FileLoader,
        loader_kwargs: Dict[str, Any] = None,
        storer: Union[str, Type[Storer]] = PromptStorer,
        storer_kwargs: Dict[str, Any] = None,
        dispatcher: Union[str, Type[Dispatcher]] = StaticDispatcher,
        dispatcher_kwargs: Dict[str, Any] = None,
    ):
        """Construct a new instance.

        :param algorithm: The solving method to solve the problem instance.
        :param algorithm_kwargs: A dict-like object containing the named parameters for the ``algorithm``'s class
            constructor.
        :param loader: The class that stores the optimized solution in a proper way.
        :param loader_kwargs: A dict-like object containing the named parameters for the ``loaders``'s class
            constructor.
        :param storer: The class that stores the optimized solution in a proper way.
        :param storer_kwargs: A dict-like object containing the named parameters for the ``storer``'s class
            constructor.
        :param dispatcher: The class that orchestrates the optimization process, linking the loaded instance to the
            algorithm, and the obtained solution to the storer.
        :param dispatcher_kwargs: A dict-like object containing the named parameters for the ``dispatcher``'s class
            constructor.
        """
        if algorithm_kwargs is None:
            algorithm_kwargs = dict()
        if loader_kwargs is None:
            loader_kwargs = dict()
        if storer_kwargs is None:
            storer_kwargs = dict()
        if dispatcher_kwargs is None:
            dispatcher_kwargs = dict()

        self._base_loader_cls = loader
        self._loader_kwargs = loader_kwargs

        self._base_algorithm_cls = algorithm
        self._algorithm_kwargs = algorithm_kwargs

        self._base_storer_cls = storer
        self._storer_kwargs = storer_kwargs

        self._base_dispatcher_cls = dispatcher
        self._dispatcher_kwargs = dispatcher_kwargs

    @property
    def _loader_cls(self) -> Type[Loader]:
        base = self._base_loader_cls
        tuned_kwargs = self._loader_kwargs

        class _TunedLoader(base):
            def __init__(self, *args, **kwargs):
                super().__init__(
                    *args, **kwargs, **tuned_kwargs,
                )

        return _TunedLoader

    @property
    def _algorithm_cls(self) -> Type[Algorithm]:
        base = self._base_algorithm_cls
        tuned_kwargs = self._algorithm_kwargs

        class _TunedAlgorithm(base):
            def __init__(self, *args, **kwargs):
                super().__init__(
                    *args, **kwargs, **tuned_kwargs,
                )

        return _TunedAlgorithm

    @property
    def _storer_cls(self) -> Type[Storer]:
        base = self._base_storer_cls
        tuned_kwargs = self._storer_kwargs

        class _TunedStorer(base):
            def __init__(self, *args, **kwargs):
                super().__init__(
                    *args, **kwargs, **tuned_kwargs,
                )

        return _TunedStorer

    @property
    def _dispatcher_cls(self) -> Type[Dispatcher]:
        base = self._base_dispatcher_cls
        tuned_kwargs = self._dispatcher_kwargs

        class _TunedDispatcher(base):
            def __init__(self, *args, **kwargs):
                super().__init__(
                    *args, **kwargs, **tuned_kwargs,
                )

        return _TunedDispatcher

    @property
    def _dispatcher(self) -> Dispatcher:
        return self._dispatcher_cls(self._loader_cls, self._algorithm_cls, self._storer_cls,)

    def solve(self) -> Result:
        """Compute an optimization.

        :return: The execution's result, containing a optimized solution for the given problem's instance.
        """
        return self._dispatcher.run()
