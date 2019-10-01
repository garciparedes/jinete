from typing import List


def remove_duplicates(seq: List) -> List:
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]
