from __future__ import annotations
from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    TYPE_CHECKING,
)
from ..models import (
    Fleet,
    Job,
    Surface,
)
from .formatters import (
    HashCodeLoaderFormatter,
)

if TYPE_CHECKING:
    from typing import (
        Type,
    )
    from .formatters import (
        LoaderFormatter,
    )


class Loader(ABC):

    def __init__(self, formatter_cls: Type[LoaderFormatter] = None):
        if formatter_cls is None:
            formatter_cls = HashCodeLoaderFormatter
        self.formatter_cls = formatter_cls
        self.formatter: LoaderFormatter = None

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
