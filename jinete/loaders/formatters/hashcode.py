from abc import ABC, abstractmethod

from ...models import (
    Fleet,
    Job,
    Surface,
)
from .abc import (
    LoaderFormatter,
)


class HashCodeLoaderFormatter(LoaderFormatter):

    @property
    def fleet(self) -> Fleet:
        pass

    @property
    def job(self) -> Job:
        pass

    @property
    def surface(self) -> Surface:
        pass
