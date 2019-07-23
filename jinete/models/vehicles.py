from __future__ import annotations

import logging
from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime, timedelta
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
    final: Position = field(default=None)
    earliest: datetime = field(default=None)
    latest: datetime = field(default=None)
    timeout: timedelta = field(default=None)
    uuid: UUID = field(default_factory=uuid4)
