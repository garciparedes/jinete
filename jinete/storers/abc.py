from abc import ABC, abstractmethod

from ..models import Planning


class Storer(ABC):

    @abstractmethod
    def store(self, planning: Planning) -> None:
        pass
