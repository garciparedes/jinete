from __future__ import annotations

from typing import (
    TYPE_CHECKING,
)

import pulp as lp

from .abc import (
    Model,
)

if TYPE_CHECKING:
    from typing import (
        List,
        Set,
    )
    from ....models import (
        Route,
    )


class ThreeIndexModel(Model):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._model = None

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
        return self._model

    @property
    def objective(self) -> lp.LpConstraintVar:
        return self._objective

    @property
    def constraints(self) -> List[lp.LpConstraint]:
        return self._constraints

    def build(self):
        # nodes = list()  # V_i | V_j
        # vehicles = list()  # K_k

        pickups = list()  # P_i
        deliveries = list()  # D_i

        times = [[]]  # t_ij
        durations = list()  # d_i
        vehicle_capacities = list()  # Q_k
        route_capacities = list()  # T_k
        loads = list()  # q_i

        time_windows = [[]]  # e_i, l_i

        # costs = [[[]]]  # c_ijk

        self._model = lp.LpProblem("3-idx_dial-a-ride", lp.LpMaximize)

        self.x = self._build_x_variables()
        self.u = self._build_u_variables()
        self.w = self._build_w_variables()
        self.r = self._build_r_variables()

        self._objective = self._build_objective()
        self._constraints = self._build_constraints()

        self._model.objective = self.objective
        self._model.extend(self.constraints)

    @property
    def vehicles(self):
        return self.fleet.vehicles

    @property
    def positions(self):
        if self._positions is None:
            self._positions = self._build_positions()
        return self._positions

    def _build_positions(self):
        origins = {trip.origin for trip in self.job.trips}
        destinations = {trip.destination for trip in self.job.trips}
        positions = tuple(origins.union(destinations))
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
        raise NotImplementedError

    def solve(self) -> Set[Route]:
        return set()
