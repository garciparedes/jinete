from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from ..loaders import (
        Loader,
    )
    from ..algorithms import (
        Algorithm,
    )
    from ..storers import (
        Storer,
    )


class Dispatcher(ABC):

    def __init__(self, loader_cls: Type[Loader], algorithm_cls: Type[Algorithm], storer_cls: Type[Storer]):
        self.loader_cls = loader_cls
        self.algorithm_cls = algorithm_cls
        self.storer_cls = storer_cls

    @abstractmethod
    def run(self):
        pass
