from abc import ABC, abstractmethod


class StorerFormatter(ABC):
    def __init__(self, planning):
        self.planning = planning

    @abstractmethod
    def format(self) -> str:
        pass
