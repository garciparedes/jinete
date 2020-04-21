"""
Contains entities to represent services in the data model.
"""

from __future__ import (
    annotations,
)

import logging
from typing import (
    TYPE_CHECKING,
)

from .abc import (
    Model,
)
from .constants import (
    MAX_FLOAT,
)

if TYPE_CHECKING:
    from typing import (
        Dict,
        Any,
        Generator,
        Tuple,
    )
    from .positions import Position

logger = logging.getLogger(__name__)


class Service(Model):
    """
    Represents the requested action to visit a specific position, having some time restrictions and costs.
    """

    __slots__ = (
        "position",
        "earliest",
        "latest",
        "duration",
    )
    position: Position
    """
    The position of the service.
    """

    earliest: float
    """
    The earliest time to start the service.

    """
    latest: float
    """
    The latest time to start the service.

    """

    duration: float
    """
    The duration to perform the service. Commonly known as the ``load_time`` in another contexts.

    """

    def __init__(self, position: Position, earliest: float = 0.0, latest: float = MAX_FLOAT, duration: float = 0.0):
        """
        The constructor of the class.

        :param position: The geometric position in which the service should be performed.
        :param earliest: The earliest time to be able to perform the service.
        :param latest: The latest time to be able to perform the service.
        :param duration: The requested time to perform the service.
        """
        self.position = position
        self.earliest = earliest
        self.latest = latest
        self.duration = duration

    def __deepcopy__(self, memo: Dict[int, Any]) -> Service:
        return self

    def __eq__(self, other: Service) -> bool:
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(tuple(self))

    def __iter__(self) -> Generator[Tuple[str, Any], None, None]:
        yield from (
            ("position", self.position),
            ("earliest", self.earliest),
            ("latest", self.latest),
            ("duration", self.duration),
        )

    def distance_to(self, other: Service) -> float:
        """
        Computes the distance from ``self`` to ``other``.

        :param other: Service to compute the distance from ``self``.
        :return: distance between ``self`` and ``other``.
        """
        return self.position.distance_to(other.position)

    def time_to(self, other: Service, *args, **kwargs) -> float:
        """
        Computes the time from ``self`` to ``other``.

        :param other: Service to compute the time from ``self``.
        :return: time between ``self`` and ``other``.
        """
        return self.position.time_to(other.position, *args, **kwargs)
