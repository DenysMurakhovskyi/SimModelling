from dataclasses import dataclass
from typing import List, Tuple
import networkx as nx
import matplotlib.pyplot as plt

from .bricks import Creator, Process, Disposer


@dataclass
class SimulationScheme:
    start_point: Creator
    elements: List[Process]
    end_point: Disposer

    def __init__(self, links: List[Tuple], number_of_processes: int = 1):
        # inputs check
        if len(links) < number_of_processes + 1:
            raise ValueError(f'The scheme is not properly connected. Links:{len(links)}, '
                             f'process: {number_of_processes}')

        if number_of_processes <= 0:
            raise ValueError('NUmber of processes should be a positive value')

        self.start_point = Creator()
        self.end_point = Disposer()
        self.elements = [Process() for _ in range(number_of_processes)]
        self.links = links

    def show_scheme(self):
        G = self._create_graph()
        nx.draw(G, with_labels=True, linewidths=3, font_size=14, node_size=600)
        plt.show()

    def _create_graph(self) -> nx.Graph:
        G = nx.DiGraph()

        # adding nodes
        G.add_node('Creator')
        for n, _ in enumerate(self.elements, start=1):
            G.add_node(f'Process_{n}')
        G.add_node('Disposer')

        # adding edges
        def name_node(node: int, total: int):
            if node == 0:
                return 'Creator'
            elif node == total:
                return 'Disposer'
            else:
                return f'Process_{node}'

        named_links = list(map(lambda x: (name_node(x[0], len(self.links)),
                                          name_node(x[1], len(self.links))),
                               self.links))
        G.add_edges_from(named_links)

        # returning graph
        return G

