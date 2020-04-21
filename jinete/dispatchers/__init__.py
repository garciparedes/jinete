"""High level scheduling during the process of optimization (feeding with new trips, updating state, etc.)."""

from .abc import (
    Dispatcher,
)
from .static import (
    StaticDispatcher,
)
