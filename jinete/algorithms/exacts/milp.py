from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import pulp as lp

from ...models import (
    Planning,
)

from ..abc import (
    Algorithm,
)

if TYPE_CHECKING:
    from typing import (
        Set,
        List,
    )
    from ...models import (
        Route,
    )

logger = logging.getLogger(__name__)


class MilpAlgorithm(Algorithm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _build_x_variables(self, nodes, vehicles) -> List[List[List[lp.LpVariable]]]:
        x = list()
        for i in range(len(nodes)):
            x_i = list()
            for j in range(len(nodes)):
                x_ij = list()
                for k in range(len(vehicles)):
                    x_ijk = lp.LpVariable(f'x[{i}][{j}][{k}]', cat=lp.LpBinary)
                    x_ij.append(x_ijk)
                x_i.append(x_ij)
            x.append(x_i)
        return x

    def _build_u_variables(self, nodes, vehicles) -> List[List[lp.LpVariable]]:
        u = list()
        for i in range(len(nodes)):
            u_i = list()
            for k in range(len(vehicles)):
                u_ik = lp.LpVariable(f'u[{i}][{k}]')
                u_i.append(u_ik)
            u.append(u_i)
        return u

    def _build_w_variables(self, nodes, vehicles) -> List[List[lp.LpVariable]]:
        w = list()
        for i in range(len(nodes)):
            w_i = list()
            for k in range(len(vehicles)):
                w_ik = lp.LpVariable(f'w[{i}][{k}]')
                w_i.append(w_ik)
            w.append(w_i)
        return w

    def _build_r_variables(self, nodes, vehicles) -> List[List[lp.LpVariable]]:
        r = list()
        for i in range(len(nodes)):
            r_i = list()
            for k in range(len(vehicles)):
                r_ik = lp.LpVariable(f'r[{i}][{k}]')
                r_i.append(r_ik)
            r.append(r_i)
        return r

    def _objective(self, x, c):
        raise NotImplementedError

    def _constrains(self, x, u, w, r):
        raise NotImplementedError

    def _optimize(self) -> Planning:
        nodes = list()  # V_i | V_j
        vehicles = list()  # K_k

        pickups = list()  # P_i
        deliveries = list()  # D_i

        times = [[]]  # t_ij
        durations = list()  # d_i
        vehicle_capacities = list()  # Q_k
        route_capacities = list()  # T_k
        loads = list()  # q_i

        time_windows = [[]]  # e_i, l_i

        costs = [[[]]]  # c_ijk

        x = self._build_x_variables(nodes, vehicles)  # x_ijk
        u = self._build_u_variables(nodes, vehicles)  # u_ik
        w = self._build_w_variables(nodes, vehicles)  # w_ik
        r = self._build_r_variables(nodes, vehicles)  # r_ik

        # Create model
        model = lp.LpProblem("3-idx_dial-a-ride", lp.LpMaximize)

        # Variables
        model.objective = self._objective(x, costs)
        model.extend(self._constrains(x, u, w, r))

        # Optimize
        model.solve()

        # Print the value of the objective
        print("Objective = %f" % lp.value(model.objective))

        routes: Set[Route] = set()
        return Planning(routes)
