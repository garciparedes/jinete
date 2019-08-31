from __future__ import annotations
from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    TYPE_CHECKING,
    Any)
from ..models import (
    Fleet,
    Job,
    Surface,
)
from .formatters import (
    CordeauLaporteLoaderFormatter,
)

if TYPE_CHECKING:
    from typing import (
        Type,
        Optional,
    )
    from .formatters import (
        LoaderFormatter,
    )


class Loader(ABC):
    formatter_cls: Type[LoaderFormatter]
    _formatter: Optional[LoaderFormatter]

    def __init__(self, formatter_cls: Type[LoaderFormatter] = None):
        if formatter_cls is None:
            formatter_cls = CordeauLaporteLoaderFormatter
        self.formatter_cls = formatter_cls
        self._formatter = None

    @property
    def formatter(self) -> LoaderFormatter:
        if self._formatter is None:
            self._formatter = self.formatter_cls(self.data)
        return self._formatter

    @property
    @abstractmethod
    def data(self) -> Any:
        pass

    @property
    @abstractmethod
    def fleet(self) -> Fleet:
        pass

    @property
    @abstractmethod
    def job(self) -> Job:
        pass

    @property
    @abstractmethod
    def surface(self) -> Surface:
        pass
