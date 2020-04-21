"""Set of algorithms based on the formulation off Mixed-Integer Linear Programming models."""

from __future__ import (
    annotations,
)

import logging
from typing import (
    TYPE_CHECKING,
)

from ...models import (
    Planning,
)
from ..abc import (
    Algorithm,
)
from .models import (
    ThreeIndexLinearModel,
)

if TYPE_CHECKING:
    from typing import Type
    from .models import LinearModel

logger = logging.getLogger(__name__)


class MilpAlgorithm(Algorithm):
    """The `jinete`'s interface to solve the given problem, supported by the Mixed-Integer Linear Programming frame."""

    def __init__(self, model_cls: Type[LinearModel] = None, *args, **kwargs):
        """Construct a new instance.

        :param model_cls: The model class to generate the representation of the problem.
        :param args: Additional positional arguments.
        :param kwargs: Additional named arguments.
        """
        super().__init__(*args, **kwargs)

        if model_cls is None:
            model_cls = ThreeIndexLinearModel

        self.model_cls = model_cls

        self.args = args
        self.kwargs = kwargs

    def _build_model(self) -> LinearModel:
        return self.model_cls(*self.args, **self.kwargs)

    def _optimize(self) -> Planning:
        model = self._build_model()

        routes = model.solve()

        return Planning(routes)
