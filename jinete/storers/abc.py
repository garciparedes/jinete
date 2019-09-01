from __future__ import annotations

import logging
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from typing import (
        Type,
        Set,
    )
    from ..models import (
        Result,
        Route,
        Trip,
    )
    from .formatters import (
        StorerFormatter,
    )

logger = logging.getLogger(__name__)


class Storer(ABC):

    def __init__(self, result: Result, formatter_cls: Type[StorerFormatter] = None):
        if formatter_cls is None:
            from .formatters import ColumnarStorerFormatter
            formatter_cls = ColumnarStorerFormatter
        self.result = result
        self.formatter_cls = formatter_cls

    def formatted_planning(self) -> str:
        return self.formatter_cls(result=self.result).format()

    @property
    def trips(self) -> Set[Trip]:
        return self.result.trips

    @property
    def routes(self) -> Set[Route]:
        return self.result.routes

    @abstractmethod
    def store(self) -> None:
        pass
