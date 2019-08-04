from .abc import (
    Algorithm,
)
from ..models import (
    Planning,
)


class NaiveAlgorithm(Algorithm):

    def optimize(self) -> Planning:
        routes = dict()
        return Planning(routes)
