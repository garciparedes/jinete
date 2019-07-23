from random import uniform, randint
from typing import Set

import jinete as jit


def generate_one_position(x_min: float = -100, x_max: float = 100, y_min: float = -100,
                          y_max: float = 100) -> jit.XYPosition:
    return jit.XYPosition(lat=uniform(x_min, x_max), lon=uniform(y_min, y_max))


def generate_positions(n: int, *args, **kwargs) -> Set[jit.XYPosition]:
    return {
        generate_one_position(*args, **kwargs) for _ in range(n)
    }


def generate_one_trip(earliest_min: float = 0, earliest_max: float = 86400, timeout_min: float = 1800,
                      timeout_max: float = 7200, load_time_min: float = 300, load_time_max: float = 900,
                      capacity_min: int = 1, capacity_max: int = 3, *args, **kwargs) -> jit.Trip:
    origin, destination = tuple(generate_positions(2, *args, **kwargs))
    earliest = uniform(earliest_min, earliest_max)
    timeout = uniform(timeout_min, timeout_max)
    capacity = randint(capacity_min, capacity_max)
    load_time = uniform(load_time_min, load_time_max)
    return jit.Trip(origin, destination, earliest, timeout, load_time, capacity)


def generate_trips(n: int, *args, **kwargs) -> Set[jit.Trip]:
    return {
        generate_one_trip(*args, **kwargs) for _ in range(n)
    }


def generate_one_planned_trip(feasible: bool, *args, **kwargs) -> jit.PlannedTrip:
    trip = generate_one_trip(*args, **kwargs)

    # TODO: Improve feasible randomness.
    if feasible:
        collection_time = trip.earliest
        delivery_time = trip.latest
    else:
        collection_time = trip.earliest - 3600
        delivery_time = trip.latest + 3600

    return jit.PlannedTrip(trip, collection_time, delivery_time)


def generate_planned_trips(n: int, *args, **kwargs) -> Set[jit.PlannedTrip]:
    return {
        generate_one_planned_trip(*args, **kwargs) for _ in range(n)
    }


def generate_one_vehicle(capacity_min: int = 1, capacity_max: int = 3, earliest_min: float = 0,
                         earliest_max: float = 86400, timeout_min: float = 14400, timeout_max: float = 28800,
                         *args, **kwargs) -> jit.Vehicle:
    # TODO: Increase parameter options.
    capacity = randint(capacity_min, capacity_max)
    initial = generate_one_position(*args, **kwargs)
    earliest = uniform(earliest_min, earliest_max)
    timeout = uniform(timeout_min, timeout_max)
    return jit.Vehicle(initial, capacity=capacity, earliest=earliest, timeout=timeout)


def generate_vehicles(n: int, *args, **kwargs) -> Set[jit.Vehicle]:
    return {
        generate_one_vehicle(*args, **kwargs) for _ in range(n)
    }


def generate_one_route(feasible: bool, planned_trips_min: int = 1, planned_trips_max: int = 20,
                       *args, **kwargs) -> jit.Route:
    vehicle = generate_one_vehicle(*args, **kwargs)

    planned_trips_len = randint(planned_trips_min, planned_trips_max)
    planned_trips = list()
    cut_len = vehicle.timeout / planned_trips_len

    planned_trip = generate_one_planned_trip(feasible, earliest_min=vehicle.earliest + 1,
                                             earliest_max=vehicle.earliest + 1, timeout_min=cut_len - 1,
                                             timeout_max=cut_len - 1)

    planned_trips.append(jit.PlannedTrip.empty(
        vehicle.earliest, vehicle.earliest + 1, vehicle.initial, planned_trip.origin
    ))
    planned_trips.append(planned_trip)

    for i in range(planned_trips_len):
        cut_min = vehicle.earliest + cut_len * i

        planned_trip = generate_one_planned_trip(feasible, earliest_min=cut_min, earliest_max=cut_min,
                                                 timeout_min=cut_len - 1, timeout_max=cut_len - 1)
        planned_trips.append(jit.PlannedTrip.empty(
            planned_trips[-1].delivery_time, planned_trips[-1].delivery_time + 1,
            planned_trips[-1].destination, planned_trip.origin
        ))

        planned_trips.append(planned_trip)

    planned_trips.append(jit.PlannedTrip.empty(
        planned_trips[-1].delivery_time, planned_trips[-1].delivery_time + 1,
        planned_trips[-1].destination, vehicle.final
    ))

    planned_trips = tuple(planned_trips)

    route = jit.Route(planned_trips, vehicle)
    return route


def generate_routes(n: int, *args, **kwargs) -> Set[jit.Route]:
    return {
        generate_one_route(*args, **kwargs) for _ in range(n)
    }
