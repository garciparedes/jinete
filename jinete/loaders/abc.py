from abc import ABC, abstractmethod

from ..models import (
    Fleet,
    Job,
)


class Loader(ABC):

    @property
    @abstractmethod
    def fleet(self) -> Fleet:
        pass

    @property
    @abstractmethod
    def job(self) -> Job:
        pass
