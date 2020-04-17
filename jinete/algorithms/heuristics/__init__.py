"""Set of solving methods with reasonable space and time complexity."""

from .insertion import (
    InsertionAlgorithm,
    InsertionIterator,
    StatelessInsertionIterator,
    BestStatelessInsertionIterator,
    RankingInsertionIterator,
    InsertionStrategy,
    SamplingInsertionStrategy,
    IntensiveInsertionStrategy,
    TailInsertionStrategy,
)
from .local_search import (
    LocalSearchAlgorithm,
    LocalSearchStrategy,
    OneShiftLocalSearchStrategy,
    TwoOPTLocalSearchStrategy,
    ReallocationLocalSearchStrategy,
)
