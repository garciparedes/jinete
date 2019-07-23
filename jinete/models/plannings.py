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
    from .surfaces import (
        Surface,
    )

logger = logging.getLogger(__name__)


@dataclass
class Planning(object):
    routes: Set[Route]
    surface: Surface
    uuid: UUID = field(default_factory=uuid4)
