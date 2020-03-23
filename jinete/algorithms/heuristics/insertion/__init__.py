"""Set of route generation methods."""

from .algorithm import (
    InsertionAlgorithm,
)
from .iterators import (
    InsertionIterator,
    StatelessInsertionIterator,
    BestStatelessInsertionIterator,
    RankingInsertionIterator,
)
from .strategies import (
    InsertionStrategy,
    SamplingInsertionStrategy,
    IntensiveInsertionStrategy,
    TailInsertionStrategy,
)
