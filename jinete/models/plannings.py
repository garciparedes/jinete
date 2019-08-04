from __future__ import annotations

import logging
from dataclasses import (
    dataclass,
    field,
)
from typing import (
    TYPE_CHECKING,
    Set,
    Optional)
from uuid import (
    uuid4,
)

if TYPE_CHECKING:
    from .routes import (
        Route,
    )
    from uuid import (
        UUID,
    )
    from .surfaces import (
        Surface,
    )

logger = logging.getLogger(__name__)


@dataclass
class Planning(object):
    routes: Set[Route]
    computation_time: float = field(default=0)
    surface: Optional[Surface] = field(default=None)
    uuid: UUID = field(default_factory=uuid4)
