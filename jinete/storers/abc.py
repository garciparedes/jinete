"""The set of abstract definitions for the ``storers`` module."""

from __future__ import (
    annotations,
)

import logging
from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    TYPE_CHECKING,
)

from cached_property import (
    cached_property,
)

if TYPE_CHECKING:
    from typing import (
        Type,
        Set,
    )
    from ..models import (
        Result,
        Route,
        Trip,
    )
    from .formatters import StorerFormatter

logger = logging.getLogger(__name__)


class Storer(ABC):
    """Store a resulting solution."""

    def __init__(self, result: Result, formatter_cls: Type[StorerFormatter] = None):
        """Construct a new object instance.

        :param result: The result object to store.
        :param formatter_cls: The formatter class to be used during the storage process.
        """
        if formatter_cls is None:
            from .formatters import ColumnarStorerFormatter

            formatter_cls = ColumnarStorerFormatter
        self.result = result
        self.formatter_cls = formatter_cls

    @cached_property
    def _formatted(self) -> str:
        return self.formatter_cls(result=self.result).format()

    @property
    def _trips(self) -> Set[Trip]:
        return self.result.trips

    @property
    def _routes(self) -> Set[Route]:
        return self.result.routes

    @abstractmethod
    def store(self) -> None:
        """Perform a storage process."""
        pass
