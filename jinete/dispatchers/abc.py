from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

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

    def __init__(self, loader: Loader, algorithm: Algorithm, storer: Storer):
        self.loader = loader
        self.algorithm = algorithm
        self.storer = storer
