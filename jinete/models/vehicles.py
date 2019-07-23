from __future__ import annotations

import logging
from dataclasses import (
    dataclass,
    field,
)
from sys import maxsize
from typing import (
    TYPE_CHECKING,
)
from uuid import (
    uuid4,
)

if TYPE_CHECKING:
    from uuid import (
        UUID,
    )
from .positions import (
    Position,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Vehicle(object):
    initial: Position
    capacity: int = field(default=1)
    _final: Position = field(default=None)
    earliest: float = field(default=0.0)
    timeout: float = field(default=None)
    uuid: UUID = field(default_factory=uuid4)

    @property
    def latest(self) -> float:
        if self.timeout is None:
            return maxsize
        return self.earliest + self.timeout

    @property
    def final(self) -> Position:
        if self._final is None:
            return self.initial
        return self._final
