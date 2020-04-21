"""
Abstract base classes used as base for the entities implemented on :mod:`~jinete.models` module.
"""

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
    from typing import (
        Any,
        Generator,
        Tuple,
    )


class Model(ABC):
    """
    The abstract model class. The function of this class is to provide common methods such us casting or printing
    functionality used by all the implemented models of the library.

    .. seealso:: classes
        :py:class:`~jinete.models.jobs.Job`,
        :py:class:`~jinete.models.planned_trips.PlannedTrip`,
        :py:class:`~jinete.models.plannings.Planning`,
        :py:class:`~jinete.models.positions.Position`,
        :py:class:`~jinete.models.positions.GeometricPosition`,
        :py:class:`~jinete.models.results.Result`,
        :py:class:`~jinete.models.routes.Route`,
        :py:class:`~jinete.models.services.Service`,
        :py:class:`~jinete.models.stops.Stop`,
        :py:class:`~jinete.models.surfaces.Surface`,
        :py:class:`~jinete.models.trips.Trip`,
        :py:class:`~jinete.models.vehicles.Fleet`,
        :py:class:`~jinete.models.vehicles.Vehicle`,
    """

    def __init__(self):
        """
        The constructor of the class.
        """

    def __repr__(self):
        return self._print(dict(self))

    def _print(self, values):
        values = ", ".join(f"{key}={value}" for key, value in values.items())
        return f"{self.__class__.__name__}({values})"

    def _print_key_value(self, key: str, value: Any):
        return f"{key}={value}"

    @abstractmethod
    def __iter__(self) -> Generator[Tuple[str, Any], None, None]:
        pass
