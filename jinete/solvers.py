from __future__ import annotations

from typing import TYPE_CHECKING

from .loaders import (
    FileLoader,
)
from .algorithms import (
    InsertionAlgorithm,
)
from .storers import (
    PromptStorer,
)
from .dispatchers import (
    StaticDispatcher,
)

if TYPE_CHECKING:
    from typing import (
        Type,
        Union,
        Dict,
        Any,
    )
    from .loaders import (
        Loader,
    )
    from .algorithms import (
        Algorithm,
    )
    from .models import (
        Result,
    )
    from .storers import (
        Storer,
    )
    from .dispatchers import (
        Dispatcher,
    )


class Solver(object):

    def __init__(self,
                 algorithm: Union[str, Type[Algorithm]] = InsertionAlgorithm,
                 algorithm_kwargs: Dict[str, Any] = None,
                 loader: Union[str, Type[Loader]] = FileLoader,
                 loader_kwargs: Dict[str, Any] = None,
                 storer: Union[str, Type[Storer]] = PromptStorer,
                 storer_kwargs: Dict[str, Any] = None,
                 dispatcher: Union[str, Type[Dispatcher]] = StaticDispatcher,
                 dispatcher_kwargs: Dict[str, Any] = None):
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

        class TunedLoader(base):
            def __init__(self, *args, **kwargs):
                super().__init__(
                    *args, **kwargs,
                    **tuned_kwargs,
                )

        return TunedLoader

    @property
    def _algorithm_cls(self) -> Type[Algorithm]:
        base = self._base_algorithm_cls
        tuned_kwargs = self._algorithm_kwargs

        class TunedAlgorithm(base):
            def __init__(self, *args, **kwargs):
                super().__init__(
                    *args, **kwargs,
                    **tuned_kwargs,
                )

        return TunedAlgorithm

    @property
    def _storer_cls(self) -> Type[Storer]:
        base = self._base_storer_cls
        tuned_kwargs = self._storer_kwargs

        class TunedStorer(base):
            def __init__(self, *args, **kwargs):
                super().__init__(
                    *args, **kwargs,
                    **tuned_kwargs,
                )

        return TunedStorer

    @property
    def _dispatcher_cls(self) -> Type[Dispatcher]:
        base = self._base_dispatcher_cls
        tuned_kwargs = self._dispatcher_kwargs

        class TunedDispatcher(base):
            def __init__(self, *args, **kwargs):
                super().__init__(
                    *args, **kwargs,
                    **tuned_kwargs,
                )

        return TunedDispatcher

    @property
    def _dispatcher(self) -> Dispatcher:
        return self._dispatcher_cls(
            self._loader_cls,
            self._algorithm_cls,
            self._storer_cls,
        )

    def solve(self) -> Result:
        return self._dispatcher.run()
