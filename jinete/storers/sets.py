from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from .abc import (
    Storer,
)

if TYPE_CHECKING:
    from typing import (
        Set,
        Type,
    )

logger = logging.getLogger(__name__)


class StorerSet(Storer):

    def __init__(self, storer_cls_set: Set[Type[Storer]], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.storer_cls_set = storer_cls_set
        self.args = args
        self.kwargs = kwargs

    def store(self) -> None:
        for storer_cls in self.storer_cls_set:
            logger.info(f'Storing result with "{storer_cls.__name__}"...')

            storer = storer_cls(*self.args, **self.kwargs)
            storer.store()
