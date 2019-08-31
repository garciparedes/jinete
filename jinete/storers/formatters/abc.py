from __future__ import annotations
from abc import ABC, abstractmethod

from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from typing import (
        Set,
    )
    from ...models import (
        Result,
        Planning,
        Job,
        Route,
        Objective,
    )


class StorerFormatter(ABC):
    def __init__(self, result: Result, remove_empty_routes: bool = False):
        self.result = result
        self.remove_empty_routes = remove_empty_routes

    @property
    def job(self) -> Job:
        return self.result.job

    @property
    def planning(self) -> Planning:
        return self.result.planning

    @property
    def routes(self) -> Set[Route]:
        if self.remove_empty_routes:
            return self.planning.loaded_routes
        return self.planning.routes

    @property
    def objective(self) -> Objective:
        return self.result.objective

    @abstractmethod
    def format(self) -> str:
        pass
