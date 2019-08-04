from abc import ABC, abstractmethod
from typing import Type

from ..models import Planning

from .formatters import StorerFormatter


class Storer(ABC):

    def __init__(self, planning: Planning, formatter_cls: Type[StorerFormatter]):
        self.planning = planning
        self.formatter_cls = formatter_cls

    def formatted_planning(self) -> str:
        return self.formatter_cls(self.planning).format()

    @abstractmethod
    def store(self) -> None:
        pass
