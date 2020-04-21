"""The set of definitions to store results in filesystems."""

from pathlib import (
    Path,
)

from .abc import (
    Storer,
)


class FileStorer(Storer):
    """Store a resulting solution into a file."""

    def __init__(self, file_path: Path, *args, **kwargs):
        """Construct a new object instance.

        :param file_path: The file path in which to store the problem solution.
        :param args: Additional positional arguments.
        :param kwargs: Additional named arguments.
        """
        super().__init__(*args, **kwargs)
        self.file_path = file_path

    def store(self) -> None:
        """Perform a storage process."""
        with self.file_path.open("w") as file:
            text = self._formatted
            file.write(text)
