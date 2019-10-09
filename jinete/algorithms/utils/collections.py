from typing import List, TypeVar, Set

E = TypeVar('E')


def remove_duplicates(seq: List[E]) -> List[E]:
    seen: Set[E] = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]
