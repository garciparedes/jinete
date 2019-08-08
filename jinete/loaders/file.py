from __future__ import annotations

import logging
from pathlib import (
    Path,
)

from ..models import (
    Job,
    Surface,
    Fleet,
)
from .abc import (
    Loader,
)

logger = logging.getLogger(__name__)


class FileLoader(Loader):

    def __init__(self, file_path: Path, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not isinstance(file_path, Path):
            file_path = Path(file_path)

        self.file_path = file_path

        self._fleet = None
        self._job = None
        self._surface = None

    def _build_formatter(self, force: bool = True):
        if self.formatter is not None and force is False:
            return
        with self.file_path.open() as file:
            data = tuple(tuple(int(v) for v in line.split()) for line in file.readlines())
            self.formatter = self.formatter_cls(data)

    @property
    def fleet(self) -> Fleet:
        if self._fleet is None:
            self._build_formatter()
            self._fleet = self.formatter.fleet(surface=self.surface)
        return self._fleet

    @property
    def job(self) -> Job:
        if self._job is None:
            self._build_formatter()
            self._job = self.formatter.job(surface=self.surface)
        return self._job

    @property
    def surface(self) -> Surface:
        if self._surface is None:
            self._build_formatter()
            self._surface = self.formatter.surface()
        return self._surface
