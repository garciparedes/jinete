from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ..abc import (
    Algorithm,
)

if TYPE_CHECKING:
    from ...models import (
        Planning,
    )

logger = logging.getLogger(__name__)


class MilpAlgorithm(Algorithm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _optimize(self) -> Planning:
        raise NotImplementedError
