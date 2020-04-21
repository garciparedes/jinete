"""Formatting modules from raw objects to ``jinete```s class hierarchy."""

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

if TYPE_CHECKING:
    from typing import Any
    from ...models import (
        Fleet,
        Job,
        Surface,
    )


class LoaderFormatter(ABC):
    """Format a problem instance from a raw object to build ``jinete``'s set of objects."""

    def __init__(self, data: Any):
        """Construct a new instance.

        :param data: The object to retrieve the on load instance.
        """
        self.data = data

    @abstractmethod
    def fleet(self, surface: Surface, *args, **kwargs) -> Fleet:
        """Retrieve the fleet object for the current on load instance.

        :param surface: The surface surface object for the current on load instance.
        :param args: Additional positional arguments.
        :param kwargs: Additional named arguments.
        :return: A surface instance from the loaded instance.
        """
        pass

    @abstractmethod
    def job(self, surface: Surface, *args, **kwargs) -> Job:
        """Retrieve the job object for the current on load instance.

        :param surface: The surface object for the current on load instance.
        :param args: Additional positional arguments.
        :param kwargs: Additional named arguments.
        :return: A surface instance from the loaded instance.
        """
        pass

    @abstractmethod
    def surface(self, *args, **kwargs) -> Surface:
        """Retrieve the surface object for the current on load instance.

        :param args: Additional positional arguments.
        :param kwargs: Additional named arguments.
        :return: A surface instance from the loaded instance.
        """
        pass
