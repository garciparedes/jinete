from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import (
    TYPE_CHECKING,
    Optional)

from datetime import (
    datetime,
    timedelta,
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


@dataclass
class Trip(object):
    origin: Position
    destination: Position

    earliest: datetime
    timeout: Optional[timedelta] = field(default=None)

    load_time: timedelta = field(default_factory=timedelta)

    capacity: int = field(default=1)
    uuid: UUID = field(default_factory=uuid4)

    @property
    def latest(self) -> Optional[datetime]:
        if self.timeout is None:
            return None
        return self.earliest + self.timeout
