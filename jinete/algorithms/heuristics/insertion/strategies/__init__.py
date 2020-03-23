"""Decision logic about how to insert trips."""

from .abc import (
    InsertionStrategy,
)
from .intensive import (
    IntensiveInsertionStrategy,
)
from .sampling import (
    SamplingInsertionStrategy,
)
from .tail import (
    TailInsertionStrategy,
)
