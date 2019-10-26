from __future__ import annotations

from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

from ..abc import (
    Storer,
)

if TYPE_CHECKING:
    from typing import (
        Dict,
        Any,
        Tuple,
    )
    from ...models import (
        Position,
    )


class GraphPlotStorer(Storer):

    def _generate_nodes(self, edges: Dict[Tuple[Position, Position], Dict[str, Any]]) -> Dict[Position, Dict[str, Any]]:
        nodes: Dict[Position, Dict[str, Any]] = dict()
        for trip in self.trips:
            nodes[trip.origin_position] = {
                'label': f'+{trip.identifier}',
            }
            nodes[trip.destination_position] = {
                'label': f'-{trip.identifier}',
            }
        for position_pair in edges.keys():
            if position_pair[0] not in nodes:
                nodes[position_pair[0]] = {
                    'label': '',
                }
            if position_pair[1] not in nodes:
                nodes[position_pair[1]] = {
                    'label': '',
                }
        return nodes

    def _generate_edges(self) -> Dict[Tuple[Position, Position], Dict[str, Any]]:
        edges = dict()
        for route, color in zip(self.routes, sns.husl_palette(len(self.routes))):
            for first, second in zip(route.stops[:-1], route.stops[1:]):
                edges[(first.position, second.position)] = {
                    'color': color,
                    'label': '',
                }
        return edges

    def _generate_graph(self) -> nx.Graph:
        graph = nx.DiGraph()

        edges = self._generate_edges()
        graph.add_edges_from(edges.keys())
        for position_pair, metadata in edges.items():
            graph.edges[position_pair].update(metadata)

        nodes = self._generate_nodes(edges)
        graph.add_nodes_from(nodes.keys())
        for position, metadata in nodes.items():
            graph.nodes[position].update(metadata)

        return graph

    @staticmethod
    def _show_graph(graph: nx.Graph) -> None:
        import matplotlib as mpl
        mpl.rcParams['figure.dpi'] = 300

        pos = {node: node.coordinates for node in graph.nodes.keys()}

        node_labels = {node: metadata['label'] for node, metadata in graph.nodes.items()}

        edge_color = [metadata['color'] for metadata in graph.edges.values()]
        edge_labels = {edge: metadata['label'] for edge, metadata in graph.edges.items()}

        nx.draw(graph, pos=pos, edge_color=edge_color, node_size=100)
        nx.draw_networkx_labels(graph, pos, labels=node_labels, font_size=5, font_color='white')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

        plt.show()

    def store(self) -> None:
        graph = self._generate_graph()
        self._show_graph(graph)
