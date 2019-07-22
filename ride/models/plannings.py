from __future__ import annotations

import logging
from dataclasses import (
    dataclass,
    field,
)
from typing import (
    TYPE_CHECKING,
    Set,
)
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

logger = logging.getLogger(__name__)


@dataclass
class Planning(object):
    routes: Set[Route]
    uuid: UUID = field(default_factory=uuid4)
