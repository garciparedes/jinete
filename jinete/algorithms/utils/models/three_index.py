from __future__ import annotations

import logging
from collections import (
    defaultdict,
)
from itertools import (
    product,
)
from operator import (
    itemgetter,
)
from typing import (
    TYPE_CHECKING,
)

from cached_property import (
    cached_property,
)
import pulp as lp

from ....models import (
    Stop,
    Route,
    PlannedTrip,
)
from .abc import (
    Model,
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
    from ....models import (
        Trip,
        Vehicle,
        Position,
    )

logger = logging.getLogger(__name__)

BIG = 10000


class ThreeIndexModel(Model):

    def __init__(self, solver: lp.LpSolver = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.solver = solver

    @cached_property
    def problem(self) -> lp.LpProblem:
        problem = lp.LpProblem("3-idx_dial-a-ride", lp.LpMinimize)
        problem.objective = self.objective
        problem.extend(self.constraints)
        return problem

    @cached_property
    def objective(self) -> Optional[lp.LpConstraintVar]:
        return lp.lpSum(
            self.x[k][i][j] * self.costs[i][j]
            for k, i, j in product(self.routes_indexer, self.positions_indexer, self.positions_indexer)
        )

    @cached_property
    def constraints(self) -> List[lp.LpConstraint]:
        constraints: List[lp.LpConstraint] = sum([
            self.uniqueness_constraints,
            self.connectivity_constraints,
            self.time_constraints,
            self.feasibility_constraints,
        ], [])

        logger.info(f'Built "{len(constraints)}" constraints.')
        return constraints

    @cached_property
    def x(self) -> List[List[List[lp.LpVariable]]]:
        x = list()
        for k in self.routes_indexer:
            x_k = list()
            for i in self.positions_indexer:
                x_ki = list()
                for j in self.positions_indexer:
                    x_kij = lp.LpVariable(f'x_{k}_{i}_{j}', cat=lp.LpBinary)
                    x_ki.append(x_kij)
                x_k.append(x_ki)
            x.append(x_k)
        return x

    @cached_property
    def u(self) -> List[List[lp.LpVariable]]:
        u = list()
        for k in self.routes_indexer:
            u_k = list()
            for i in self.positions_indexer:
                u_ki = lp.LpVariable(f'u_{k}_{i}', lowBound=0.0)
                u_k.append(u_ki)
            u.append(u_k)
        return u

    @cached_property
    def w(self) -> List[List[lp.LpVariable]]:
        w = list()
        for k in self.routes_indexer:
            w_k = list()
            for i in self.positions_indexer:
                w_ki = lp.LpVariable(f'w_{k}_{i}', lowBound=0.0)
                w_k.append(w_ki)
            w.append(w_k)
        return w

    @cached_property
    def vehicles(self) -> Tuple[Vehicle, ...]:
        return tuple(self.fleet.vehicles)

    @cached_property
    def trips(self) -> Tuple[Trip, ...]:
        return tuple(self.job.trips)

    @cached_property
    def positions(self) -> Tuple[Position, ...]:
        origins = tuple(trip.origin_position for trip in self.trips)
        destinations = tuple(trip.destination_position for trip in self.trips)
        positions = (
                (self.vehicles[0].origin_position,) +
                origins +
                destinations +
                (self.vehicles[0].destination_position,)
        )

        return positions

    @cached_property
    def costs(self):
        costs = list()
        for origin in self.positions:
            origin_costs = list()
            for destination in self.positions:
                if origin == destination:
                    cost = BIG
                else:
                    cost = origin.distance_to(destination)
                origin_costs.append(cost)
            costs.append(origin_costs)
        return costs

    @property
    def pickups_indexer(self) -> Iterable[int]:
        return range(1, self.n + 1)

    @property
    def nodes_indexer(self) -> Iterable[int]:
        return range(1, self.n * 2 + 1)

    @property
    def routes_indexer(self) -> Iterable[int]:
        return range(len(self.vehicles))

    @property
    def positions_indexer(self) -> Iterable[int]:
        return range(len(self.positions))

    @property
    def n(self) -> int:
        return len(self.trips)

    def trip_by_position_idx(self, idx: int) -> Optional[Trip]:
        if idx in (0, len(self.positions) - 1):
            return None
        return self.trips[(idx % self.n) - 1]

    def time_window_by_position_idx(self, idx: int) -> Tuple[float, float]:
        position = self.positions[idx]
        trip = self.trip_by_position_idx(idx)
        if trip is None:
            earliest, latest = 0, 1440
        elif position == trip.origin_position:
            earliest, latest = trip.origin_earliest, trip.origin_latest
        elif position == trip.destination_position:
            earliest, latest = trip.destination_earliest, trip.destination_latest
        else:
            raise Exception(f'There was a problem related with earliest, latest indices.')
        return earliest, latest

    def capacity_by_position_idx(self, idx: int) -> float:
        trip = self.trip_by_position_idx(idx)
        if trip is None:
            return 0

        capacity = trip.capacity
        if not idx < len(self.positions) / 2:
            capacity *= -1

        return capacity

    def load_time_by_position_idx(self, idx: int) -> float:
        trip = self.trip_by_position_idx(idx)
        if trip is None:
            return 0
        return trip.origin_duration

    def timeout_by_position_idx(self, idx: int) -> float:
        trip = self.trip_by_position_idx(idx)
        if trip is None:
            return 0
        return trip.timeout

    @cached_property
    def uniqueness_constraints(self) -> List[lp.LpConstraint]:
        constraints = list()

        for i in self.pickups_indexer:
            lhs = lp.lpSum(
                self.x[k][i][j]
                for j, k in product(self.positions_indexer, self.routes_indexer)
            )
            constraints.append(lhs == 1)

            for k in self.routes_indexer:
                lhs = (
                        lp.lpSum(self.x[k][i][j] for j in self.positions_indexer) -
                        lp.lpSum(self.x[k][self.n + i][j] for j in self.positions_indexer)
                )
                constraints.append(lhs == 0)

        return constraints

    @cached_property
    def connectivity_constraints(self) -> List[lp.LpConstraint]:
        constraints = list()

        for k in self.routes_indexer:
            lhs = lp.lpSum(self.x[k][0][j] for j in self.positions_indexer)
            constraints.append(lhs == 1)

            for i in self.nodes_indexer:
                lhs = (
                        lp.lpSum(self.x[k][j][i] for j in self.positions_indexer) -
                        lp.lpSum(self.x[k][i][j] for j in self.positions_indexer)
                )
                constraints.append(lhs == 0)

            lhs = lp.lpSum(self.x[k][i][-1] for i in self.positions_indexer)
            constraints.append(lhs == 1)

        return constraints

    @cached_property
    def time_constraints(self) -> List[lp.LpConstraint]:
        constraints = list()

        for k in self.routes_indexer:
            for i, j in product(self.positions_indexer, self.positions_indexer):
                load_time_i = self.load_time_by_position_idx(i)
                travel_time = self.positions[i].time_to(self.positions[j])

                earliest_i, latest_i = self.time_window_by_position_idx(i)
                earliest_j, latest_j = self.time_window_by_position_idx(j)

                cons = max(0, latest_i + load_time_i + travel_time - earliest_j)

                constraints.append(
                    self.u[k][j] >= self.u[k][i] + load_time_i + travel_time - cons * (1 - self.x[k][i][j]),
                )

                capacity_i = self.capacity_by_position_idx(i)
                capacity_j = self.capacity_by_position_idx(j)

                cons = self.vehicles[k].capacity + min(0.0, capacity_i)

                constraints.append(
                    self.w[k][j] >= self.w[k][i] + capacity_j - cons * (1 - self.x[k][i][j]),
                )

        return constraints

    @cached_property
    def feasibility_constraints(self) -> List[lp.LpConstraint]:
        constraints = list()
        for k in self.routes_indexer:
            constraint = self.u[k][-1] - self.u[k][0] <= self.vehicles[k].timeout
            constraints.append(constraint)

            for i in self.positions_indexer:
                earliest, latest = self.time_window_by_position_idx(i)

                constraints.extend([
                    earliest <= self.u[k][i],
                    self.u[k][i] <= latest,
                ])

            for i in self.pickups_indexer:
                load_time = self.load_time_by_position_idx(i)
                timeout = self.timeout_by_position_idx(i)
                travel_time = self.positions[i].time_to(self.positions[i + self.n])

                constraints.extend([
                    travel_time <= self.u[k][i + self.n] - (self.u[k][i] + load_time),
                    self.u[k][i + self.n] - (self.u[k][i] + load_time) <= timeout,
                ])

            for i in self.positions_indexer:
                capacity = self.capacity_by_position_idx(i)

                constraints.extend([
                    max(0.0, capacity) <= self.w[k][i],
                    self.w[k][i] <= self.vehicles[k].capacity + min(0.0, capacity),
                ])

        return constraints

    def solve(self) -> Set[Route]:
        logger.info('Starting to solve...')
        self.problem.solve(self.solver)

        self.validate()
        logger.info(f'Obtained "{lp.value(self.objective)}" reaching "{lp.LpStatus[self.problem.status]}".')
        return self._solution_to_routes()

    def print_solution(self):
        print('X:')
        for k in self.routes_indexer:
            print(f'Vehicle {k}-th.')
            print(f'   {" ".join(map(lambda num: f"{num:02d}", self.positions_indexer))}')
            for i in self.positions_indexer:
                print(f'{i:02d}', end=' ')
                for j in self.positions_indexer:
                    print(f'{int(self.x[k][i][j].varValue):2d}', end=' ')
                print()
            print()

        print('U:')
        for k in self.routes_indexer:
            print(f'Vehicle {k}-th.')
            for i in self.positions_indexer:
                print(f'{self.u[k][i].varValue:4.01f}', end=' ')
            print()

        print('W:')
        for k in self.routes_indexer:
            print(f'Vehicle {k}-th.')
            for i in self.positions_indexer:
                print(f'{self.w[k][i].varValue:4.01f}', end=' ')
            print()

    def validate(self):
        for k in self.routes_indexer:
            for i in self.positions_indexer:
                logger.info(f'Obtained "u[{k}][{i}]={self.u[k][i].varValue}".')
                assert self.u[k][i].varValue >= 0.0

                logger.info(f'Obtained "w[{k}][{i}]={self.w[k][i].varValue}".')
                assert self.w[k][i].varValue >= 0.0

                for j in self.positions_indexer:
                    logger.info(f'Obtained "x[{k}][{i}][{j}]={self.x[k][i][j].varValue}".')
                    assert min(abs(self.x[k][i][j].varValue), abs(self.x[k][i][j].varValue - 1)) <= 0.05

    def _solution_to_routes(self):
        logger.info(f'Casting solution to a set of routes...')
        routes = set()
        for k in self.routes_indexer:
            route = Route(self.vehicles[k])

            ordered_trip_indexes = [
                idx
                for idx, u_k in sorted(enumerate(u_k.varValue for u_k in self.u[k]), key=itemgetter(1))
            ]

            positions = self._solution_to_positions(k, ordered_trip_indexes)
            stops = self._positions_to_stops(route, positions)
            trips = self._positions_to_trips(positions)
            self._build_planned_trips(route, trips, stops)

            for stop in stops:
                route.append_stop(stop)

            route.finish()
            routes.add(route)
        return routes

    def _positions_to_trips(self, positions) -> List[Trip]:
        trips: List[Trip] = list()
        for position in positions:
            trip = next((trip for trip in self.trips if trip.origin_position == position), None)
            if trip is None:
                continue
            if trip in trips:
                continue
            trips.append(trip)
        return trips

    def _build_planned_trips(self, route: Route, trips: List[Trip], stops: List[Stop]) -> List[PlannedTrip]:
        stop_mapper = self._stop_to_stop_mapper(stops)

        planned_trips = list()
        for trip in trips:
            pickup = stop_mapper[trip.origin_position].pop(0)
            delivery = stop_mapper[trip.destination_position].pop(0)

            planned_trip = PlannedTrip(route, trip, pickup, delivery)
            planned_trips.append(planned_trip)
        return planned_trips

    def _solution_to_positions(self, k, ordered_trip_indexes) -> List[Position]:
        positions = list()
        for i, j in product(ordered_trip_indexes, self.positions_indexer):
            if not int(self.x[k][i][j].varValue) == 1:
                continue
            positions.append(self.positions[i])
        return positions

    def _positions_to_stops(self, route, positions) -> List[Stop]:
        stops = [route.first_stop]
        for position in positions:
            pickup = Stop(route, position, stops[-1])
            stops.append(pickup)
        stops.pop(0)
        return stops

    def _stop_to_stop_mapper(self, stops: List[Stop]) -> Dict[Position, List[Stop]]:
        mapper: Dict[Position, List[Stop]] = defaultdict(list)
        for stop in stops:
            mapper[stop.position].append(stop)
        return mapper
