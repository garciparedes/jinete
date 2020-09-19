"""Three index linear model class definitions."""

from __future__ import (
    annotations,
)

import logging
from collections import (
    defaultdict,
)
from itertools import (
    product,
)
from typing import (
    TYPE_CHECKING,
)

import pulp as lp
from cached_property import (
    cached_property,
)
from jinete.models import (
    PlannedTrip,
    Route,
    Stop,
)

from .abc import (
    LinearModel,
)

if TYPE_CHECKING:
    from typing import (
        List,
        Set,
        Tuple,
        Iterable,
        Optional,
        Dict,
    )
    from jinete.models import (
        Trip,
        Vehicle,
        Position,
    )

logger = logging.getLogger(__name__)

BIG = 10000


class ThreeIndexLinearModel(LinearModel):
    """Three index model class implementation.

    This implementation is based on the Cordeau-Laporte paper about the dial-a-ride problem.
    """

    def __init__(self, solver: lp.LpSolver = None, *args, **kwargs):
        """Construct a new object instance.

        :param solver: The solver to be used during the optimization.
        :param args: Additional positional arguments.
        :param kwargs: Additional named arguments.
        """
        super().__init__(*args, **kwargs)
        self.solver = solver

    @cached_property
    def _problem(self) -> lp.LpProblem:
        problem = lp.LpProblem("3-idx_dial-a-ride", lp.LpMinimize)
        problem.objective = self._objective
        problem.extend(self._constraints)
        return problem

    @cached_property
    def _objective(self) -> Optional[lp.LpConstraintVar]:
        return lp.lpSum(
            self._x[k][i][j] * self._costs[i][j]
            for k, i, j in product(self._routes_indexer, self._positions_indexer, self._positions_indexer)
        )

    @cached_property
    def _constraints(self) -> List[lp.LpConstraint]:
        constraints: List[lp.LpConstraint] = sum(
            [
                self._uniqueness_constraints,
                self._connectivity_constraints,
                self._time_constraints,
                self._feasibility_constraints,
            ],
            [],
        )

        logger.info(f'Built "{len(constraints)}" constraints.')
        return constraints

    @cached_property
    def _x(self) -> List[List[List[lp.LpVariable]]]:
        x = list()
        for k in self._routes_indexer:
            x_k = list()
            for i in self._positions_indexer:
                x_ki = list()
                for j in self._positions_indexer:
                    x_kij = lp.LpVariable(f"x_{k}_{i}_{j}", cat=lp.LpBinary)
                    x_ki.append(x_kij)
                x_k.append(x_ki)
            x.append(x_k)
        return x

    @cached_property
    def _u(self) -> List[List[lp.LpVariable]]:
        u = list()
        for k in self._routes_indexer:
            u_k = list()
            for i in self._positions_indexer:
                u_ki = lp.LpVariable(f"u_{k}_{i}", lowBound=0.0)
                u_k.append(u_ki)
            u.append(u_k)
        return u

    @cached_property
    def _w(self) -> List[List[lp.LpVariable]]:
        w = list()
        for k in self._routes_indexer:
            w_k = list()
            for i in self._positions_indexer:
                w_ki = lp.LpVariable(f"w_{k}_{i}", lowBound=0.0)
                w_k.append(w_ki)
            w.append(w_k)
        return w

    @cached_property
    def _vehicles(self) -> Tuple[Vehicle, ...]:
        return tuple(self.fleet.vehicles)

    @cached_property
    def _trips(self) -> Tuple[Trip, ...]:
        return tuple(self.job.trips)

    @cached_property
    def _positions(self) -> Tuple[Position, ...]:
        origins = tuple(trip.origin_position for trip in self._trips)
        destinations = tuple(trip.destination_position for trip in self._trips)
        positions = (
            (self._vehicles[0].origin_position,) + origins + destinations + (self._vehicles[0].destination_position,)
        )

        return positions

    @cached_property
    def _costs(self):
        costs = list()
        for origin in self._positions:
            origin_costs = list()
            for destination in self._positions:
                if origin == destination:
                    cost = BIG
                else:
                    cost = origin.distance_to(destination)
                origin_costs.append(cost)
            costs.append(origin_costs)
        return costs

    @property
    def _pickups_indexer(self) -> Iterable[int]:
        return range(1, self._n + 1)

    @property
    def _nodes_indexer(self) -> Iterable[int]:
        return range(1, self._n * 2 + 1)

    @property
    def _routes_indexer(self) -> Iterable[int]:
        return range(len(self._vehicles))

    @property
    def _positions_indexer(self) -> Iterable[int]:
        return range(len(self._positions))

    @property
    def _n(self) -> int:
        return len(self._trips)

    def _trip_by_position_idx(self, idx: int) -> Optional[Trip]:
        if idx in (0, len(self._positions) - 1):
            return None
        return self._trips[(idx % self._n) - 1]

    def _idx_by_position(self, position: Position):
        return self._positions.index(position)

    def _time_window_by_position_idx(self, idx: int) -> Tuple[float, float]:
        position = self._positions[idx]
        trip = self._trip_by_position_idx(idx)
        if trip is None:
            earliest, latest = 0, 1440
        elif position == trip.origin_position:
            earliest, latest = trip.origin_earliest, trip.origin_latest
        elif position == trip.destination_position:
            earliest, latest = trip.destination_earliest, trip.destination_latest
        else:
            raise Exception("There was a problem related with earliest, latest indices.")
        return earliest, latest

    def _capacity_by_position_idx(self, idx: int) -> float:
        trip = self._trip_by_position_idx(idx)
        if trip is None:
            return 0

        capacity = trip.capacity
        if not idx < len(self._positions) / 2:
            capacity *= -1

        return capacity

    def _load_time_by_position_idx(self, idx: int) -> float:
        trip = self._trip_by_position_idx(idx)
        if trip is None:
            return 0
        return trip.origin_duration

    def _timeout_by_position_idx(self, idx: int) -> float:
        trip = self._trip_by_position_idx(idx)
        if trip is None:
            return 0
        return trip.timeout

    @cached_property
    def _uniqueness_constraints(self) -> List[lp.LpConstraint]:
        constraints = list()

        for i in self._pickups_indexer:
            lhs = lp.lpSum(self._x[k][i][j] for j, k in product(self._positions_indexer, self._routes_indexer))
            constraints.append(lhs == 1)

            for k in self._routes_indexer:
                lhs = lp.lpSum(self._x[k][i][j] for j in self._positions_indexer) - lp.lpSum(
                    self._x[k][self._n + i][j] for j in self._positions_indexer
                )
                constraints.append(lhs == 0)

        return constraints

    @cached_property
    def _connectivity_constraints(self) -> List[lp.LpConstraint]:
        constraints = list()

        for k in self._routes_indexer:
            lhs = lp.lpSum(self._x[k][0][j] for j in self._positions_indexer)
            constraints.append(lhs == 1)

            for i in self._nodes_indexer:
                lhs = lp.lpSum(self._x[k][j][i] for j in self._positions_indexer) - lp.lpSum(
                    self._x[k][i][j] for j in self._positions_indexer
                )
                constraints.append(lhs == 0)

            lhs = lp.lpSum(self._x[k][i][-1] for i in self._positions_indexer)
            constraints.append(lhs == 1)

        return constraints

    @cached_property
    def _time_constraints(self) -> List[lp.LpConstraint]:
        constraints = list()

        for k in self._routes_indexer:
            for i, j in product(self._positions_indexer, self._positions_indexer):
                load_time_i = self._load_time_by_position_idx(i)
                travel_time = self._positions[i].time_to(self._positions[j])

                earliest_i, latest_i = self._time_window_by_position_idx(i)
                earliest_j, latest_j = self._time_window_by_position_idx(j)

                cons = max(0, latest_i + load_time_i + travel_time - earliest_j)

                constraints.append(
                    self._u[k][j] >= self._u[k][i] + load_time_i + travel_time - cons * (1 - self._x[k][i][j]),
                )

                capacity_i = self._capacity_by_position_idx(i)
                capacity_j = self._capacity_by_position_idx(j)

                cons = self._vehicles[k].capacity + min(0.0, capacity_i)

                constraints.append(self._w[k][j] >= self._w[k][i] + capacity_j - cons * (1 - self._x[k][i][j]),)

        return constraints

    @cached_property
    def _feasibility_constraints(self) -> List[lp.LpConstraint]:
        constraints = list()
        for k in self._routes_indexer:
            constraint = self._u[k][-1] - self._u[k][0] <= self._vehicles[k].timeout
            constraints.append(constraint)

            for i in self._positions_indexer:
                earliest, latest = self._time_window_by_position_idx(i)

                constraints.extend([earliest <= self._u[k][i], self._u[k][i] <= latest])

            for i in self._pickups_indexer:
                load_time = self._load_time_by_position_idx(i)
                timeout = self._timeout_by_position_idx(i)
                travel_time = self._positions[i].time_to(self._positions[i + self._n])

                constraints.extend(
                    [
                        travel_time <= self._u[k][i + self._n] - (self._u[k][i] + load_time),
                        self._u[k][i + self._n] - (self._u[k][i] + load_time) <= timeout,
                    ]
                )

            for i in self._positions_indexer:
                capacity = self._capacity_by_position_idx(i)

                constraints.extend(
                    [
                        max(0.0, capacity) <= self._w[k][i],
                        self._w[k][i] <= self._vehicles[k].capacity + min(0.0, capacity),
                    ]
                )

        return constraints

    def solve(self) -> Set[Route]:
        """Perform a optimization based on the linear model.

        :return A set of optimized routes.
        """
        logger.info("Starting to solve...")
        self._problem.solve(self.solver)

        self._validate()
        logger.info(f'Obtained "{lp.value(self._objective)}" reaching "{lp.LpStatus[self._problem.status]}".')
        return self._solution_to_routes()

    def _print_solution(self):
        print("X:")
        for k in self._routes_indexer:
            print(f"Vehicle {k}-th.")
            print(f'   {" ".join(map(lambda num: f"{num:02d}", self._positions_indexer))}')
            for i in self._positions_indexer:
                print(f"{i:02d}", end=" ")
                for j in self._positions_indexer:
                    print(f"{int(self._x[k][i][j].varValue):2d}", end=" ")
                print()
            print()

        print("U:")
        for k in self._routes_indexer:
            print(f"Vehicle {k}-th.")
            for i in self._positions_indexer:
                print(f"{self._u[k][i].varValue:4.01f}", end=" ")
            print()

        print("W:")
        for k in self._routes_indexer:
            print(f"Vehicle {k}-th.")
            for i in self._positions_indexer:
                print(f"{self._w[k][i].varValue:4.01f}", end=" ")
            print()

    def _validate(self):
        for k in self._routes_indexer:
            for i in self._positions_indexer:
                logger.info(f'Obtained "u[{k}][{i}]={self._u[k][i].varValue}".')
                assert self._u[k][i].varValue >= 0.0

                logger.info(f'Obtained "w[{k}][{i}]={self._w[k][i].varValue}".')
                assert self._w[k][i].varValue >= 0.0

                for j in self._positions_indexer:
                    logger.info(f'Obtained "x[{k}][{i}][{j}]={self._x[k][i][j].varValue}".')
                    assert min(abs(self._x[k][i][j].varValue), abs(self._x[k][i][j].varValue - 1)) <= 0.05

    def _solution_to_routes(self):
        logger.info("Casting solution to a set of routes...")
        routes = set()
        for k in self._routes_indexer:
            vehicle = self._vehicles[k]
            route = Route(vehicle)

            positions = self._solution_to_positions(k)
            stops = self._positions_to_stops(route, positions)
            trips = self._positions_to_trips(positions)

            self._build_planned_trips(vehicle, trips, stops)
            self._adjust_waiting_times(stops, k)

            for stop in stops:
                route.insert_stop(stop)

            routes.add(route)
        return routes

    def _positions_to_trips(self, positions) -> List[Trip]:
        trips: List[Trip] = list()
        for position in positions:
            trip = next((trip for trip in self._trips if trip.origin_position == position), None)
            if trip is None:
                continue
            if trip in trips:
                continue
            trips.append(trip)
        return trips

    def _build_planned_trips(self, vehicle: Vehicle, trips: List[Trip], stops: List[Stop]) -> List[PlannedTrip]:
        stop_mapper = self._stop_to_stop_mapper(stops)

        planned_trips = list()
        for trip in trips:
            pickup = stop_mapper[trip.origin_position].pop(0)
            delivery = stop_mapper[trip.destination_position].pop(0)
            planned_trip = PlannedTrip(vehicle, trip, pickup, delivery)
            planned_trips.append(planned_trip)
        return planned_trips

    def _solution_to_positions(self, k: int) -> List[Position]:
        ordered_trip_indexes = [idx for idx in sorted(range(len(self._u[k])), key=lambda x: self._u[k][x].varValue)]

        positions = list()
        for i, j in product(ordered_trip_indexes, self._positions_indexer):
            if not int(self._x[k][i][j].varValue) == 1:
                continue
            positions.append(self._positions[i])
        return positions

    @staticmethod
    def _positions_to_stops(route, positions) -> List[Stop]:
        stops = [route.first_stop]
        for position in positions:
            if position == stops[-1].position:
                continue
            pickup = Stop(route.vehicle, position, stops[-1])
            stops.append(pickup)
        return stops

    @staticmethod
    def _stop_to_stop_mapper(stops: List[Stop]) -> Dict[Position, List[Stop]]:
        mapper: Dict[Position, List[Stop]] = defaultdict(list)
        for stop in stops:
            mapper[stop.position].append(stop)
        return mapper

    def _adjust_waiting_times(self, stops: List[Stop], k: int):
        starting_times = tuple(float(u_k.varValue) for u_k in self._u[k])
        for stop in stops:
            stop.flush()
            stop.starting_time = starting_times[self._idx_by_position(stop.position)]
