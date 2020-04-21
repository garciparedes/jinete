"""Defines the loader's abstract interface to load problem instances from external sources."""

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

from cached_property import (
    cached_property,
)

from ..models import (
    Fleet,
    Job,
    Surface,
)
from .formatters import (
    CordeauLaporteLoaderFormatter,
)

if TYPE_CHECKING:
    from typing import (
        Type,
        Any,
    )
    from .formatters import LoaderFormatter


class Loader(ABC):
    """Load a problem instance from external sources and build the needed class hierarchy to generate solutions."""

    def __init__(self, formatter_cls: Type[LoaderFormatter] = None):
        """Construct a new instance.

        :param formatter_cls: The formatter from raw data to the problem instance's class hierarchy.
        """
        if formatter_cls is None:
            formatter_cls = CordeauLaporteLoaderFormatter
        self._formatter_cls = formatter_cls

    @property
    @abstractmethod
    def _data(self) -> Any:
        pass

    @cached_property
    def _formatter(self) -> LoaderFormatter:
        return self._formatter_cls(self._data)

    @property
    @abstractmethod
    def fleet(self) -> Fleet:
        """Retrieve the fleet object for the current on load instance.

        :return: A surface instance from the loaded instance.
        """
        pass

    @property
    @abstractmethod
    def job(self) -> Job:
        """Retrieve the job object for the current on load instance.

        :return: A surface instance from the loaded instance.
        """
        pass

    @property
    @abstractmethod
    def surface(self) -> Surface:
        """Retrieve the surface object for the current on load instance.

        :return: A surface instance from the loaded instance.
        """
        pass
