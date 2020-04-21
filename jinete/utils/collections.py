"""A set of utilities related with collections."""

from __future__ import (
    annotations,
)

from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from typing import (
        List,
        TypeVar,
        Set,
    )

    E = TypeVar("E")


def remove_duplicates(seq: List[E]) -> List[E]:
    """Remove the duplicated elements of a list, preserving its original order.

    :param seq: The original list.
    :return: A list with elements ordered as a in the initial one, but removing the duplicated elements.
    """
    seen: Set[E] = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]
