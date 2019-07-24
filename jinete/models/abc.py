from abc import ABC, abstractmethod
from typing import Any, Dict


class Model(ABC):
    def __repr__(self):
        return self._print(self.as_dict())

    def _print(self, values):
        values = ', '.join(f'{key}={value}' for key, value in values.items())
        return f'{self.__class__.__name__}({values})'

    @abstractmethod
    def as_dict(self) -> Dict[str, Any]:
        pass
