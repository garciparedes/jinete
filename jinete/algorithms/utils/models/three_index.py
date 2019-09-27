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

        self._model = lp.LpProblem("3-idx_dial-a-ride", lp.LpMaximize)

        self.x = self._build_x_variables(nodes, vehicles)
        self.u = self._build_u_variables(nodes, vehicles)
        self.w = self._build_w_variables(nodes, vehicles)
        self.r = self._build_r_variables(nodes, vehicles)

        self._objective = self._build_objective()
        self._constraints = self._build_constraints()

        self._model.objective = self.objective
        self._model.extend(self.constraints)

    @staticmethod
    def _build_x_variables(nodes, vehicles) -> List[List[List[lp.LpVariable]]]:
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

    @staticmethod
    def _build_u_variables(nodes, vehicles) -> List[List[lp.LpVariable]]:
        u = list()
        for i in range(len(nodes)):
            u_i = list()
            for k in range(len(vehicles)):
                u_ik = lp.LpVariable(f'u[{i}][{k}]')
                u_i.append(u_ik)
            u.append(u_i)
        return u

    @staticmethod
    def _build_w_variables(nodes, vehicles) -> List[List[lp.LpVariable]]:
        w = list()
        for i in range(len(nodes)):
            w_i = list()
            for k in range(len(vehicles)):
                w_ik = lp.LpVariable(f'w[{i}][{k}]')
                w_i.append(w_ik)
            w.append(w_i)
        return w

    @staticmethod
    def _build_r_variables(nodes, vehicles) -> List[List[lp.LpVariable]]:
        r = list()
        for i in range(len(nodes)):
            r_i = list()
            for k in range(len(vehicles)):
                r_ik = lp.LpVariable(f'r[{i}][{k}]')
                r_i.append(r_ik)
            r.append(r_i)
        return r

    def _build_objective(self) -> lp.LpConstraintVar:
        raise NotImplementedError

    def _build_constraints(self) -> List[lp.LpConstraint]:
        raise NotImplementedError

    def solve(self) -> Set[Route]:
        return set()
