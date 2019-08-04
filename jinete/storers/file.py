from pathlib import Path

from .abc import Storer


class FileStorer(Storer):

    def __init__(self, file_path: Path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_path = file_path

    def store(self) -> None:
        with self.file_path.open('w') as file:
            text = self.formatted_planning()
            file.write(text)
