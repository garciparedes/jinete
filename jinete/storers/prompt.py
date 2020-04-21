"""The set of definitions to store results as a prompt message."""

from .abc import (
    Storer,
)


class PromptStorer(Storer):
    """Store a resulting solution as a prompt message."""

    def store(self) -> None:
        """Perform a storage process."""
        text = self._formatted
        print(text)
