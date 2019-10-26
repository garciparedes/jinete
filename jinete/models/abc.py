from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import (
        Any,
        Generator,
        Tuple,
    )


class Model(ABC):
    def __repr__(self):
        return self._print(dict(self))

    def _print(self, values):
        values = ', '.join(f'{key}={value}' for key, value in values.items())
        return f'{self.__class__.__name__}({values})'

    def _print_key_value(self, key: str, value: Any):
        return f'{key}={value}'

    @abstractmethod
    def __iter__(self) -> Generator[Tuple[str, Any], None, None]:
        pass
