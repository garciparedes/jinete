from __future__ import annotations

import logging
from itertools import product
from operator import itemgetter
from typing import (
    TYPE_CHECKING,
)

import pulp as lp

from ....models import (
    MAX_INT,
    Stop,
    Route,
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
    )
    from ....models import (
        Trip,
        Vehicle,
    )

logger = logging.getLogger(__name__)


class ThreeIndexModel(Model):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.args = args
        self.kwargs = kwargs

        self._trips = None
        self._vehicles = None

        self._problem = None

        self.x = None
        self.u = None
        self.w = None
        self.r = None

        self._objective = None
        self._constraints = None

        self._positions = None
        self._costs = None

        self.build()

    @property
    def problem(self) -> lp.LpProblem:
        return self._problem

    @property
    def objective(self) -> lp.LpConstraintVar:
        return self._objective

    @property
    def constraints(self) -> List[lp.LpConstraint]:
        return self._constraints

    def build(self):
        self._problem = lp.LpProblem("3-idx_dial-a-ride", lp.LpMinimize)

        self.x = self._build_x_variables()
        self.u = self._build_u_variables()
        self.w = self._build_w_variables()
        self.r = self._build_r_variables()

        self._objective = self._build_objective()
        self._constraints = self._build_constraints()

        self._problem.objective = self.objective
        self._problem.extend(self.constraints)

    @property
    def vehicles(self) -> Tuple[Vehicle]:
        if self._vehicles is None:
            self._vehicles = tuple(self.fleet.vehicles)
        return self._vehicles

    @property
    def trips(self) -> Tuple[Trip]:
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
                    cost = MAX_INT
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
            for i in self.positions_indexer:
                r_ki = lp.LpVariable(f'r{k}_{i}', lowBound=0.0)
                r_k.append(r_ki)
            r.append(r_k)
        return r

    def _build_objective(self) -> lp.LpConstraintVar:
        return sum(
            self.x[k][i][j] * self.costs[i][j]
            for k, i, j in product(self.routes_indexer, self.positions_indexer, self.positions_indexer)
        )

    def _build_constraints(self) -> List[lp.LpConstraint]:
        return sum([
            self._build_uniqueness_constraints(),
            self._build_connectivity_constraints(),
            self._build_time_constraints(),
            self._build_feasibility_constraints(),
            self._build_variable_constraints(),
        ], [])

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

    def _build_uniqueness_constraints(self) -> List[lp.LpConstraint]:
        constraints = list()

        for i in self.pickups_indexer:
            lhs = sum(self.x[k][i][j] for j, k in product(self.positions_indexer, self.routes_indexer))
            constraints.append(lhs == 1)

            for k in self.routes_indexer:
                lhs = (
                        sum(self.x[k][i][j] for j in self.positions_indexer) -
                        sum(self.x[k][self.n + i][j] for j in self.positions_indexer)
                )
                constraints.append(lhs == 0)

        return constraints

    def _build_connectivity_constraints(self) -> List[lp.LpConstraint]:
        constraints = list()

        for k in self.routes_indexer:
            lhs = sum(self.x[k][0][j] for j in self.positions_indexer)
            rhs = sum(self.x[k][i][-1] for i in self.positions_indexer)
            constraints.append(lhs == rhs)

            constraints.append(lhs == 1)
            constraints.append(rhs == 1)

            for i in self.nodes_indexer:
                lhs = (
                        sum(self.x[k][i][j] for j in self.positions_indexer) -
                        sum(self.x[k][j][i] for j in self.positions_indexer)
                )
                constraints.append(lhs == 0)

        return constraints

    def _build_time_constraints(self) -> List[lp.LpConstraint]:
        constraints = list()

        for k in self.routes_indexer:
            for i in self.pickups_indexer:
                if i not in (0, len(self.positions) - 1):
                    load_time = self.trips[(i % self.n) - 1].load_time
                else:
                    load_time = 0

                constraint = self.r[k][i] >= self.u[k][i + self.n] - (self.u[k][i] + load_time)
                constraints.append(constraint)

            for i, j in product(self.positions_indexer, self.positions_indexer):
                if i not in (0, len(self.positions) - 1):
                    load_time = self.trips[(i % self.n) - 1].load_time
                else:
                    load_time = 0
                travel_time = self.positions[i].time_to(self.positions[j])

                aux = lp.LpVariable(f'aux_{k}_{i}_{j}_1', lowBound=0.0)

                aux_constraint_1 = aux <= MAX_INT * self.x[k][i][j]
                aux_constraint_2 = aux <= self.u[k][i]
                aux_constraint_3 = aux >= self.u[k][i] - (1 - self.x[k][i][j]) * MAX_INT

                constraint = self.u[k][j] >= aux + (load_time + travel_time) * self.x[k][i][j]

                constraints.extend([aux_constraint_1, aux_constraint_2, aux_constraint_3, constraint])

                if i not in (0, len(self.positions) - 1):
                    capacity = self.trips[(j % self.n) - 1].capacity
                    if not j < len(self.positions) / 2:
                        capacity *= -1
                else:
                    capacity = 0

                aux = lp.LpVariable(f'aux_{k}_{i}_{j}_2', lowBound=0.0)

                aux_constraint_1 = aux <= MAX_INT * self.x[k][i][j]
                aux_constraint_2 = aux <= self.w[k][i]
                aux_constraint_3 = aux >= self.w[k][i] - (1 - self.x[k][i][j]) * MAX_INT

                constraint = self.w[k][j] >= aux + capacity * self.x[k][i][j]

                constraints.extend([aux_constraint_1, aux_constraint_2, aux_constraint_3, constraint])

        return constraints

    def _build_feasibility_constraints(self) -> List[lp.LpConstraint]:
        constraints = list()
        for k in self.routes_indexer:
            constraint = self.u[k][-1] - self.u[k][0] <= self.vehicles[k].route_timeout
            constraints.append(constraint)

            for i in self.pickups_indexer:
                travel_time = self.positions[i].time_to(self.positions[i + self.n])
                constraint_1 = travel_time <= self.r[k][i]
                constraint_2 = self.r[k][i] <= self.vehicles[k].trip_timeout
                constraints.extend([constraint_1, constraint_2])

            for i in self.positions_indexer:
                if i not in (0, len(self.positions) - 1):
                    capacity = self.trips[(i % self.n) - 1].capacity
                    if not i < len(self.positions) / 2:
                        capacity *= -1
                else:
                    capacity = 0

                constraint = max(0, capacity) <= self.w[k][i] <= self.vehicles[k].capacity + min(0, capacity)
                constraints.append(constraint)

                if i in (0, len(self.positions) - 1):
                    continue

                trip = self.trips[(i % self.n) - 1]
                if not trip.inbound and self.positions[i] == trip.origin:
                    constraint = trip.earliest <= self.u[k][i] <= trip.latest
                    constraints.append(constraint)
                elif trip.inbound and self.positions[i] == trip.destination:
                    constraint = trip.earliest <= self.u[k][i] <= trip.latest
                    constraints.append(constraint)
                else:
                    pass
        return constraints

    def _build_variable_constraints(self) -> List[lp.LpConstraint]:
        constraints = list()

        for k in self.routes_indexer:
            for i in self.positions_indexer:
                constraints.append(0 <= self.u[k][i])
                constraints.append(0 <= self.w[k][i])
                constraints.append(0 <= self.r[k][i])

                for j in self.positions_indexer:
                    constraints.append(0 <= self.x[k][i][j] <= 1)

        return constraints

    def solve(self) -> Set[Route]:
        logger.info('Starting to solve...')
        solver = lp.LpSolverDefault
        self.problem.solve(solver)

        for k in self.routes_indexer:
            print(f'Vehicle {k}-th.')
            for i in self.positions_indexer:
                for j in self.positions_indexer:
                    print(f'{int(self.x[k][i][j].varValue)}', end=' ')
                print()
            print()

        logger.info(f'Obtained "{lp.value(self.objective)}" reaching "{lp.LpStatus[self.problem.status]}".')
        return self._solution_to_routes()

    def _solution_to_routes(self):
        logger.info(f'Casting solution to a set of routes...')
        routes = set()
        for k in self.routes_indexer:
            route = Route(self.vehicles[k])

            ordered_trip_indexes = [
                idx
                for idx, u_k in sorted(enumerate(u_k.varValue for u_k in self.u[k]), key=itemgetter(1))
                if u_k != 0.0
            ]

            for i in ordered_trip_indexes:
                for j in range(1, len(self.positions)):
                    if not min(abs(self.x[k][i][j].varValue), abs(self.x[k][i][j].varValue - 1)) <= 0.1:
                        raise Exception

                    if not int(self.x[k][i][j].varValue) == 1:
                        continue

                    origin = self.positions[i]
                    # destination = self.positions[j]

                    pickup = Stop(route, origin, route.last_stop)
                    # delivery = Stop(route, destination, pickup)
                    # trip = self.trips[(i % self.n) - 1]
                    # if trip.origin != origin or trip.destination != destination:
                    #     continue
                    # planned_trip = PlannedTrip(route=route, trip=trip, pickup=pickup, delivery=delivery)
                    route.append_stop(pickup)
                    # route.append_stop(delivery)
                    # route.append_planned_trip(planned_trip)

            route.finish()
            routes.add(route)
        return routes
