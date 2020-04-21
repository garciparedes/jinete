"""
Contains entities to represent positions in the data model.
"""

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

from .abc import (
    Model,
)

if TYPE_CHECKING:
    from typing import (
        Tuple,
        Sequence,
        Generator,
        Dict,
        Any,
    )
    from .surfaces import Surface

logger = logging.getLogger(__name__)


class Position(Model, ABC):
    """
    Represents a point on the ``Surface`` to which belongs.
    """

    def __init__(self, surface: Surface):
        """
        Constructor of the class.

        :param surface: The surface to which the position belongs.
        """
        self.surface = surface

    def distance_to(self, other: Position) -> float:
        """
        Computes the distance from ``self`` to ``other``.

        :param other: Position to compute the distance from ``self``.
        :return: distance between ``self`` and ``other``.
        """
        return self.surface.distance(self, other)

    @property
    @abstractmethod
    def coordinates(self) -> Tuple[Any]:
        """
        The coordinated representation of ``self``.

        :return: The coordinated representation of ``self``.
        """

        pass

    def time_to(self, other: Position, now: float = None) -> float:
        """
        Computes the time from ``self`` to ``other``.

        :param other: Position to compute the time from ``self``.
        :param now: The time at starting time (to model starting time dependent duration).
        :return: time between ``self`` and ``other``.
        """
        return self.surface.time(self, other, now=now)

    def __deepcopy__(self, memo: Dict[int, Any]) -> Position:
        return self


class GeometricPosition(Position):
    """
    Represents a geometric point on the ``Surface`` to which belongs.
    """

    __slots__ = ("coordinates",)

    coordinates: Tuple[float, ...]
    """
    The coordinated representation of ``self``.
    """

    def __init__(self, coordinates: Sequence[float], *args, **kwargs):
        """
        :param coordinates: The coordinates which identifies the position.
        :param args: Additional positional parameters.
        :param kwargs: Additional named parameters.
        """
        super().__init__(*args, **kwargs)
        self.coordinates = tuple(coordinates)

    def __hash__(self):
        return hash(self.coordinates)

    def __eq__(self, other) -> bool:
        return self.coordinates == other.coordinates

    def __ne__(self, other) -> bool:
        return self.coordinates != other.coordinates

    def __iter__(self) -> Generator[Tuple[str, Any], None, None]:
        yield from (("coordinates", self.coordinates),)

    def __str__(self):
        c = ",".join(f"{x:07.3f}" for x in self.coordinates)
        return f"({c})"

    def __getitem__(self, item):
        return self.coordinates[item]
