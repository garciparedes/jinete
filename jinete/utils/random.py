import itertools as it
import operator as op
from functools import (
    reduce,
)
from random import (
    Random,
)
from typing import (
    Iterable,
    Tuple,
)


def ncr(n, r):
    """
    Based on: https://stackoverflow.com/a/4941932/3921457
    :param n:
    :param r:
    :return:
    """
    r = min(r, n - r)
    numer = reduce(op.mul, range(n, n - r, -1), 1)
    denom = reduce(op.mul, range(1, r + 1), 1)
    return numer // denom


def sample_index_pairs(n: int, count: int, random: Random = None) -> Iterable[Tuple[int, int]]:
    if random is None:
        from random import randint as generator
    else:
        generator = random.randint

    maximum = ncr(n, 2)
    if maximum <= count:
        indices = it.combinations(range(n), 2)
    else:
        indices = set()
        while len(indices) < count:
            sampled_i = generator(0, n - 2)
            sampled_j = generator(sampled_i + 1, n - 1)
            pair = (sampled_i, sampled_j)
            indices.add(pair)
    return indices
