from random import uniform
from typing import Set

from rider import (
    XYPosition,
)


def generate_positions(n: int, *args, **kwargs) -> Set[XYPosition]:
    return {
        generate_one_position(*args, **kwargs) for _ in range(n)
    }


def generate_one_position(x_min: float = -100, x_max: float = 100, y_min: float = -100,
                          y_max: float = 100) -> XYPosition:
    return XYPosition(lat=uniform(x_min, x_max), lon=uniform(y_min, y_max))
