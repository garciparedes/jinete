from abc import ABC, abstractmethod
from typing import Type

from ..models import Result

from .formatters import StorerFormatter


class Storer(ABC):

    def __init__(self, result: Result, formatter_cls: Type[StorerFormatter]):
        self.result = result
        self.formatter_cls = formatter_cls

    def formatted_planning(self) -> str:
        return self.formatter_cls(self.result).format()

    @abstractmethod
    def store(self) -> None:
        pass
