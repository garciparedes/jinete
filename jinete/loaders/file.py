from __future__ import annotations

import logging
from pathlib import (
    Path,
)
from typing import TYPE_CHECKING

from ..models import (
    Job,
    Surface,
    Fleet,
)
from .abc import (
    Loader,
)

if TYPE_CHECKING:
    from typing import (
        Optional,
    )

logger = logging.getLogger(__name__)


class FileLoader(Loader):
    _fleet: Optional[Fleet]
    _job: Optional[Job]
    _surface: Optional[Surface]

    def __init__(self, file_path: Path, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not isinstance(file_path, Path):
            file_path = Path(file_path)

        self.file_path = file_path

        self._fleet = None
        self._job = None
        self._surface = None

    @property
    def data(self):
        with self.file_path.open() as file:
            data = list(list(float(v) for v in line.split()) for line in file.readlines())
        return data

    @property
    def fleet(self) -> Fleet:
        if self._fleet is None:
            self._fleet = self.formatter.fleet(surface=self.surface)
        return self._fleet

    @property
    def job(self) -> Job:
        if self._job is None:
            self._job = self.formatter.job(surface=self.surface)
        return self._job

    @property
    def surface(self) -> Surface:
        if self._surface is None:
            self._surface = self.formatter.surface()
        return self._surface
