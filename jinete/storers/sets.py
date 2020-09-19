"""The set of definitions to use more than one storer at the same time."""

from __future__ import (
    annotations,
)

import logging
from typing import (
    TYPE_CHECKING,
)

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
    """Store a resulting solution trough multiple storers.

    This implementation is an intermediate tool to combine multiple storers.
    """

    def __init__(self, storer_cls_set: Set[Type[Storer]], *args, **kwargs):
        """Construct a new object instance.

        :param storer_cls_set: The storer classes to be used to store the problem solution.
        :param args: Additional positional arguments.
        :param kwargs: Additional named arguments.
        """
        super().__init__(*args, **kwargs)
        self.storer_cls_set = storer_cls_set
        self.args = args
        self.kwargs = kwargs

    def store(self) -> None:
        """Perform a storage process."""
        for storer_cls in self.storer_cls_set:
            name = getattr(storer_cls, "__name__", None)
            logger.info(f'Storing result with "{name}"...')

            storer = storer_cls(*self.args, **self.kwargs)
            storer.store()
