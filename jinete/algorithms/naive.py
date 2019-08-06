from ..models import (
    Planning,
)
from .abc import (
    Algorithm,
)


class NaiveAlgorithm(Algorithm):

    def optimize(self) -> Planning:
        routes = set()
        return Planning(routes)
