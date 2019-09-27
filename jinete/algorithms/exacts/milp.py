from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ...models import (
    Planning,
)

from ..abc import (
    Algorithm,
)
from ..utils import (
    ThreeIndexModel,
)

if TYPE_CHECKING:
    from typing import (
        Type
    )
    from ..utils import (
        Model,
    )

logger = logging.getLogger(__name__)


class MilpAlgorithm(Algorithm):

    def __init__(self, model_cls: Type[Model] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if model_cls is None:
            model_cls = ThreeIndexModel

        self.model_cls = model_cls

        self.args = args
        self.kwargs = kwargs

    def build_model(self) -> Model:
        return self.model_cls(*self.args, **self.kwargs)

    def _optimize(self) -> Planning:
        model = self.build_model()

        routes = model.solve()

        return Planning(routes)
