from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import List, TYPE_CHECKING

from uuid import (
    uuid4,
)

if TYPE_CHECKING:
    from .vehicles import (
        Vehicle,
    )
    from .trips import (
        Trip,
    )
    from uuid import (
        UUID,
    )

logger = logging.getLogger(__name__)


@dataclass
class Route(object):
    trips: List[Trip]
    vehicle: Vehicle

    uuid: UUID = field(default_factory=uuid4)
