from datetime import datetime, timedelta
from random import uniform, randint
from typing import Set

import jinete as jit


def _uniform_td(min_td: timedelta, max_td: timedelta) -> timedelta:
    seconds = uniform(min_td.seconds, max_td.seconds)
    return timedelta(seconds=seconds)


def _uniform_dt(min_dt: datetime, max_dt: datetime) -> datetime:
    diff = max_dt - min_dt
    seconds = uniform(0, diff.seconds)
    return min_dt + timedelta(seconds=seconds)


def generate_one_position(x_min: float = -100, x_max: float = 100, y_min: float = -100,
                          y_max: float = 100) -> jit.XYPosition:
    return jit.XYPosition(lat=uniform(x_min, x_max), lon=uniform(y_min, y_max))


def generate_positions(n: int, *args, **kwargs) -> Set[jit.XYPosition]:
    return {
        generate_one_position(*args, **kwargs) for _ in range(n)
    }


def generate_one_trip(earliest_min: datetime = datetime.now(),
                      earliest_max: datetime = datetime.now() + timedelta(days=1),
                      timeout_min: timedelta = timedelta(minutes=30), timeout_max: timedelta = timedelta(hours=2),
                      load_time_min: timedelta = timedelta(minutes=5), load_time_max: timedelta = timedelta(minutes=15),
                      capacity_min: int = 1, capacity_max: int = 3, *args, **kwargs):
    origin, destination = tuple(generate_positions(2, *args, **kwargs))
    earliest = _uniform_dt(earliest_min, earliest_max)
    timeout = _uniform_td(timeout_min, timeout_max)
    capacity = randint(capacity_min, capacity_max)
    load_time = _uniform_td(load_time_min, load_time_max)
    return jit.Trip(origin, destination, earliest, timeout, load_time, capacity)


def generate_trips(n: int, *args, **kwargs) -> Set[jit.Trip]:
    return {
        generate_one_trip(*args, **kwargs) for _ in range(n)
    }


def generate_one_planned_trip(feasible: bool, *args, **kwargs) -> jit.PlannedTrip:
    pass


def generate_planned_trips(n: int, *args, **kwargs) -> Set[jit.Trip]:
    return {
        generate_one_planned_trip(*args, **kwargs) for _ in range(n)
    }


def generate_one_vehicle(capacity_min: int = 1, capacity_max: int = 3, *args, **kwargs) -> jit.Vehicle:
    # TODO: Increase parameter options.
    capacity = randint(capacity_min, capacity_max)
    initial = generate_one_position(*args, **kwargs)
    return jit.Vehicle(initial, capacity=capacity)


def generate_vehicles(n: int, *args, **kwargs) -> Set[jit.Vehicle]:
    return {
        generate_one_vehicle(*args, **kwargs) for _ in range(n)
    }


def generate_one_route(feasible: bool, *args, **kwargs) -> jit.Route:
    pass


def generate_routes(n: int, *args, **kwargs) -> Set[jit.Route]:
    return {
        generate_one_route(*args, **kwargs) for _ in range(n)
    }
