"""Defines the loader's implementation to load problem instances from files."""

from __future__ import (
    annotations,
)

import logging
from pathlib import (
    Path,
)
from typing import (
    TYPE_CHECKING,
)

from cached_property import (
    cached_property,
)

from .abc import (
    Loader,
)

if TYPE_CHECKING:
    from ..models import (
        Job,
        Surface,
        Fleet,
    )

logger = logging.getLogger(__name__)


class FileLoader(Loader):
    """Load a problem instance from a file and build the needed class hierarchy to generate solutions."""

    def __init__(self, file_path: Path, *args, **kwargs):
        """Construct a new instance.

        :param file_path: The path to load the problem instance.
        :param args: Additional positional arguments.
        :param kwargs: Additional named arguments.
        """
        super().__init__(*args, **kwargs)

        if not isinstance(file_path, Path):
            file_path = Path(file_path)

        self.file_path = file_path

        self._fleet = None
        self._job = None
        self._surface = None

    @property
    def _data(self):
        with self.file_path.open() as file:
            data = list(list(float(v) for v in line.split()) for line in file.readlines())
        return data

    @cached_property
    def fleet(self) -> Fleet:
        """Retrieve the fleet object for the current on load instance.

        :return: A surface instance from the loaded instance.
        """
        return self._formatter.fleet(surface=self.surface)

    @cached_property
    def job(self) -> Job:
        """Retrieve the job object for the current on load instance.

        :return: A surface instance from the loaded instance.
        """
        return self._formatter.job(surface=self.surface)

    @cached_property
    def surface(self) -> Surface:
        """Retrieve the surface object for the current on load instance.

        :return: A surface instance from the loaded instance.
        """
        return self._formatter.surface()
