"""The set of definitions to not to store results."""

from .abc import (
    Storer,
)


class NaiveStorer(Storer):
    """(Not) store a resulting solution.

    This entity is used mainly for testing or when the storing logic is not needed.
    """

    def store(self) -> None:
        """Perform a storage process."""
        pass
