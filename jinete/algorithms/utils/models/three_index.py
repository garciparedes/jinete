from __future__ import annotations

import logging
from collections import defaultdict
from itertools import product
from operator import itemgetter
from typing import (
    TYPE_CHECKING,
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
    _x: Optional[List[List[List[lp.LpVariable]]]]
    _r: Optional[List[List[lp.LpVariable]]]
    _u: Optional[List[List[lp.LpVariable]]]
    _w: Optional[List[List[lp.LpVariable]]]
    _objective: Optional[lp.LpConstraintVar]
    _constraints: Optional[List[lp.LpConstraint]]
    _trips: Optional[Tuple[Trip, ...]]
    _vehicles: Optional[Tuple[Vehicle, ...]]

    def __init__(self, solver: lp.LpSolver = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.solver = solver

        self._trips = None
        self._vehicles = None

        self._problem = None

        self._x = None
        self._u = None
        self._w = None
        self._r = None

        self._objective = None
        self._constraints = None

        self._positions = None
        self._costs = None

    @property
    def problem(self) -> lp.LpProblem:
        if self._problem is None:
            self._problem = self._build_problem()
        return self._problem

    @property
    def objective(self) -> Optional[lp.LpConstraintVar]:
        if self._objective is None:
            self._objective = self._build_objective()
        return self._objective

    @property
    def constraints(self) -> List[lp.LpConstraint]:
        if self._constraints is None:
            self._constraints = self._build_constraints()
        return self._constraints

    @property
    def x(self) -> List[List[List[lp.LpVariable]]]:
        if self._x is None:
            self._x = self._build_x_variables()
        return self._x

    @property
    def r(self) -> List[List[lp.LpVariable]]:
        if self._r is None:
            self._r = self._build_r_variables()
        return self._r

    @property
    def u(self) -> List[List[lp.LpVariable]]:
        if self._u is None:
            self._u = self._build_u_variables()
        return self._u

    @property
    def w(self) -> List[List[lp.LpVariable]]:
        if self._w is None:
            self._w = self._build_w_variables()
        return self._w

    @property
    def vehicles(self) -> Tuple[Vehicle, ...]:
        if self._vehicles is None:
            self._vehicles = tuple(self.fleet.vehicles)
        return self._vehicles

    @property
    def trips(self) -> Tuple[Trip, ...]:
        if self._trips is None:
            self._trips = tuple(self.job.trips)
        return self._trips

    @property
    def positions(self):
        if self._positions is None:
            self._positions = self._build_positions()
        return self._positions

    def _build_positions(self):

        origins = tuple(trip.origin for trip in self.trips)
        destinations = tuple(trip.destination for trip in self.trips)
        positions = (self.vehicles[0].initial,) + origins + destinations + (self.vehicles[0].final,)

        return positions

    @property
    def costs(self):
        if self._costs is None:
            self._costs = self._build_costs()
        return self._costs

    def _build_costs(self):
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

    def _build_x_variables(self) -> List[List[List[lp.LpVariable]]]:
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

    def _build_u_variables(self) -> List[List[lp.LpVariable]]:
        u = list()
        for k in self.routes_indexer:
            u_k = list()
            for i in self.positions_indexer:
                u_ki = lp.LpVariable(f'u_{k}_{i}', lowBound=0.0)
                u_k.append(u_ki)
            u.append(u_k)
        return u

    def _build_w_variables(self) -> List[List[lp.LpVariable]]:
        w = list()
        for k in self.routes_indexer:
            w_k = list()
            for i in self.positions_indexer:
                w_ki = lp.LpVariable(f'w_{k}_{i}', lowBound=0.0)
                w_k.append(w_ki)
            w.append(w_k)
        return w

    def _build_r_variables(self) -> List[List[lp.LpVariable]]:
        r = list()
        for k in self.routes_indexer:
            r_k = list()
            for i in self.pickups_indexer:
                r_ki = lp.LpVariable(f'r{k}_{i}', lowBound=0.0)
                r_k.append(r_ki)
            r.append(r_k)
        return r

    def _build_objective(self) -> lp.LpConstraintVar:
        return lp.lpSum(
            self.x[k][i][j] * self.costs[i][j]
            for k, i, j in product(self.routes_indexer, self.positions_indexer, self.positions_indexer)
        )

    def _build_constraints(self) -> List[lp.LpConstraint]:
        constraints: List[lp.LpConstraint] = sum([
            self._build_uniqueness_constraints(),
            self._build_connectivity_constraints(),
            self._build_time_constraints(),
            self._build_feasibility_constraints(),
        ], [])

        logger.info(f'Built "{len(constraints)}" constraints.')
        return constraints

    def _build_problem(self) -> lp.LpProblem:
        problem = lp.LpProblem("3-idx_dial-a-ride", lp.LpMinimize)
        problem.objective = self.objective
        problem.extend(self.constraints)
        return problem

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
        elif position == trip.origin:
            earliest, latest = trip.origin_earliest, trip.origin_latest
        elif position == trip.destination:
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

    def _build_uniqueness_constraints(self) -> List[lp.LpConstraint]:
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

    def _build_connectivity_constraints(self) -> List[lp.LpConstraint]:
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

    def _build_time_constraints(self) -> List[lp.LpConstraint]:
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

            for i in self.pickups_indexer:
                load_time = self.load_time_by_position_idx(i)

                constraint = self.r[k][i - 1] == self.u[k][i + self.n] - (self.u[k][i] + load_time)
                constraints.append(constraint)

        return constraints

    def _build_feasibility_constraints(self) -> List[lp.LpConstraint]:
        constraints = list()
        for k in self.routes_indexer:
            constraint = self.u[k][-1] - self.u[k][0] <= self.vehicles[k].route_timeout
            constraints.append(constraint)

            for i in self.positions_indexer:
                earliest, latest = self.time_window_by_position_idx(i)

                constraints.extend([
                    earliest <= self.u[k][i],
                    self.u[k][i] <= latest,
                ])

            for i in self.pickups_indexer:
                travel_time = self.positions[i].time_to(self.positions[i + self.n])
                constraints.extend([
                    travel_time <= self.r[k][i - 1],
                    self.r[k][i - 1] <= self.vehicles[k].trip_timeout,
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

        print('R:')
        for k in self.routes_indexer:
            print(f'Vehicle {k}-th.')
            for i in self.pickups_indexer:
                print(f'{self.r[k][i - 1].varValue:4.01f}', end=' ')
            print()

    def validate(self):
        for k in self.routes_indexer:
            for i in self.pickups_indexer:
                logger.info(f'Obtained "r[{k}][{i - 1}={self.r[k][i - 1].varValue}".')
                assert self.r[k][i - 1].varValue >= 0.0

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
            trip = next((trip for trip in self.trips if trip.origin == position), None)
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
            pickup = stop_mapper[trip.origin].pop(0)
            delivery = stop_mapper[trip.destination].pop(0)

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
