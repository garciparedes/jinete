from abc import ABC, abstractmethod
from typing import Any

from ...models import (
    Fleet,
    Job,
    Surface,
)


class LoaderFormatter(ABC):
    def __init__(self, data: Any):
        self.data = data

    @abstractmethod
    def fleet(self, surface: Surface, *args, **kwargs) -> Fleet:
        pass

    @abstractmethod
    def job(self, surface: Surface, *args, **kwargs) -> Job:
        pass

    @abstractmethod
    def surface(self, *args, **kwargs) -> Surface:
        pass
