from __future__ import annotations

import logging
from itertools import product
from typing import (
    TYPE_CHECKING,
)

import pulp as lp

from ....models import (
    MAX_INT,
    Stop,
    PlannedTrip,
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
    )
    from ....models import (
        Trip,
        Vehicle,
    )

logger = logging.getLogger(__name__)


class ThreeIndexModel(Model):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        # nodes = list()  # V_i | V_j
        # vehicles = list()  # K_k

        # pickups = list()  # P_i
        # deliveries = list()  # D_i
        #
        # times = [[]]  # t_ij
        # durations = list()  # d_i
        # vehicle_capacities = list()  # Q_k
        # route_capacities = list()  # T_k
        # loads = list()  # q_i
        #
        # time_windows = [[]]  # e_i, l_i

        # costs = [[[]]]  # c_ijk

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

    @staticmethod
    def remove_duplicates(seq):
        seen = set()
        seen_add = seen.add
        return tuple(x for x in seq if not (x in seen or seen_add(x)))

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
        for i in range(len(self.positions)):
            x_i = list()
            for j in range(len(self.positions)):
                x_ij = list()
                for k in range(len(self.vehicles)):
                    x_ijk = lp.LpVariable(f'x_{i}_{j}_{k}', cat=lp.LpBinary)
                    x_ij.append(x_ijk)
                x_i.append(x_ij)
            x.append(x_i)
        return x

    def _build_u_variables(self) -> List[List[lp.LpVariable]]:
        u = list()
        for i in range(len(self.positions)):
            u_i = list()
            for k in range(len(self.vehicles)):
                u_ik = lp.LpVariable(f'u_{i}_{k}')
                u_i.append(u_ik)
            u.append(u_i)
        return u

    def _build_w_variables(self) -> List[List[lp.LpVariable]]:
        w = list()
        for i in range(len(self.positions)):
            w_i = list()
            for k in range(len(self.vehicles)):
                w_ik = lp.LpVariable(f'w_{i}_{k}')
                w_i.append(w_ik)
            w.append(w_i)
        return w

    def _build_r_variables(self) -> List[List[lp.LpVariable]]:
        r = list()
        for i in range(len(self.positions)):
            r_i = list()
            for k in range(len(self.vehicles)):
                r_ik = lp.LpVariable(f'r{i}_{k}')
                r_i.append(r_ik)
            r.append(r_i)
        return r

    def _build_objective(self) -> lp.LpConstraintVar:
        obj = None
        for i in range(len(self.positions)):
            for j in range(len(self.positions)):
                for k in range(len(self.vehicles)):
                    obj += self.x[i][j][k] * self.costs[i][j]
        return obj

    def _build_constraints(self) -> List[lp.LpConstraint]:
        return sum([
            self._build_uniqueness_constraints(),
            self._build_connectivity_constraints(),
            self._build_time_constraints(),
            self._build_feasibility_constraints(),
        ], [])

    def _build_uniqueness_constraints(self) -> List[lp.LpConstraint]:
        constraints = list()

        for i in range(1, len(self.trips) + 1):
            lhs = sum(self.x[i][j][k] for j, k in product(range(len(self.positions)), range(len(self.vehicles))))
            constraints.append(lhs == 1)

        for i in range(1, len(self.trips) + 1):
            for k in range(len(self.vehicles)):
                lhs = (
                        sum(self.x[i][j][k] for j in range(len(self.positions))) -
                        sum(self.x[len(self.trips) + i][j][k] for j in range(len(self.positions)))
                )
                constraints.append(lhs == 0)

        return constraints

    def _build_connectivity_constraints(self) -> List[lp.LpConstraint]:
        constraints = list()

        for k in range(len(self.vehicles)):
            lhs = sum(self.x[0][j][k] for j in range(len(self.positions)))
            rhs = sum(self.x[i][-1][k] for i in range(len(self.positions)))
            constraints.append(lhs == rhs)

            constraints.append(lhs == 1)
            constraints.append(rhs == 1)

        for i in range(1, len(self.trips) * 2 + 1):
            for k in range(len(self.vehicles)):
                lhs = (
                        sum(self.x[i][j][k] for j in range(len(self.positions))) -
                        sum(self.x[j][i][k] for j in range(len(self.positions)))
                )
                constraints.append(lhs == 0)

        return constraints

    def _build_time_constraints(self) -> List[lp.LpConstraint]:
        constraints = list()

        return constraints

    def _build_feasibility_constraints(self) -> List[lp.LpConstraint]:
        constraints = list()

        return constraints

    def solve(self) -> Set[Route]:
        logger.info('Starting to solve...')
        solver = lp.LpSolverDefault
        self.problem.solve(solver)

        routes = set()
        for k in range(len(self.vehicles)):
            route = Route(self.vehicles[k])

            for i in range(1, len(self.positions)):
                for j in range(1, len(self.positions)):
                    if int(self.x[i][j][k].varValue) == 1:
                        origin = self.positions[i]
                        destination = self.positions[j]

                        pickup = Stop(route, origin, route.last_stop)
                        delivery = Stop(route, destination, pickup)
                        trip = self.trips[(i % len(self.trips)) - 1]
                        planned_trip = PlannedTrip(route=route, trip=trip, pickup=pickup, delivery=delivery)
                        route.append_planned_trip(planned_trip)
            routes.add(route)

        for k in range(len(self.vehicles)):
            print(f'Vehicle {k}-th.')
            for i in range(len(self.positions)):
                for j in range(len(self.positions)):
                    print(f'{int(self.x[i][j][k].varValue)}', end=' ')
                print()
            print()

        logger.info(f'Obtained "{lp.value(self.objective)}" reaching "{lp.LpStatus[self.problem.status]}".')
        return routes
