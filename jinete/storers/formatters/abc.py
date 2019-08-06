from abc import ABC, abstractmethod

from ...models import (
    Result,
    Planning,
    Job,
)


class StorerFormatter(ABC):
    def __init__(self, result: Result):
        self.result = result

    @property
    def job(self) -> Job:
        return self.result.job

    @property
    def planning(self) -> Planning:
        return self.result.planning

    @abstractmethod
    def format(self) -> str:
        pass
