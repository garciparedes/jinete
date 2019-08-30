from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx
import itertools as it
from ..abc import (
    Storer,
)


class GraphPlotStorer(Storer):

    def store(self) -> None:

        nodes = dict(
            it.chain.from_iterable(
                (
                    (trip.origin.coordinates, trip.origin.coordinates),
                    (trip.destination.coordinates, trip.destination.coordinates),
                )
                for trip in self.result.trips
            )
        )
        edges = dict(
            it.chain.from_iterable(
                (
                    ((first.position.coordinates, second.position.coordinates), color)
                    for first, second in zip(route.stops[:-1], route.stops[1:])
                )
                for route, color in zip(self.result.routes, ("red", "blue", "black"))
            )
        )

        for edge in edges.keys():
            nodes[edge[0]] = edge[0]
            nodes[edge[1]] = edge[1]

        # edges = {
        #    (0, 1): "red",
        #    (1, 2): "red",
        #     (0, 2): "blue",
        #    (2, 3): "red",
        # }
        X = nx.DiGraph()
        X.add_nodes_from(nodes.keys())
        X.add_edges_from(edges.keys())

        for n, p in nodes.items():
            X.nodes[n]['pos'] = p

        edge_colors = [edges[(u, v)] for u, v in X.edges]

        nx.draw(
            X,
            nodes,
            edge_color=edge_colors,
            node_size=25,

        )

        plt.show()
        pass
