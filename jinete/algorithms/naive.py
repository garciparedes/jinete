"""Naive algorithm definitions."""

from __future__ import (
    annotations,
)

from typing import (
    TYPE_CHECKING,
)

from ..models import (
    Planning,
)
from .abc import (
    Algorithm,
)

if TYPE_CHECKING:
    from typing import Set
    from ..models import Route


class NaiveAlgorithm(Algorithm):
    """Naive algorithm implementation.

    This class always returns empty results. It's main use is for internal testing.
    """

    def _optimize(self) -> Planning:
        routes: Set[Route] = set()
        return Planning(routes)
