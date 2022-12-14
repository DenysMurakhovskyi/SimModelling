from typing import List, Tuple, NoReturn
import networkx as nx
import matplotlib.pyplot as plt

from .bricks import Creator, Process, Disposer


class SimulationScheme:
    _start_point: Creator
    _elements: List[Process]
    _end_point: Disposer

    def __init__(self, links: List[Tuple], number_of_processes: int = 1):
        # inputs check
        if len(links) < number_of_processes + 1:
            raise ValueError(f'The _scheme is not properly connected. Links:{len(links)}, '
                             f'process: {number_of_processes}')

        if number_of_processes <= 0:
            raise ValueError('Number of processes should be a positive value')

        self._start_point = Creator()
        self._end_point = Disposer()
        self._elements = [Process(n) for n in range(number_of_processes)]
        self._links = links

        self._connect_scheme()

    @property
    def all_elements(self):
        return sum([[self._start_point], self._elements, [self._end_point]], [])

    @property
    def processes(self):
        return self._elements

    def show_scheme(self) -> NoReturn:
        """
        Represents the _scheme as a directed graph
        """
        G = self._create_graph()
        nx.draw(G, with_labels=True, linewidths=3, font_size=14, node_size=600)
        plt.show()

    def _create_graph(self) -> nx.DiGraph:
        """
        Creates networkX graph to show
        :return: directed graph instance
        """
        G = nx.DiGraph()

        # adding nodes
        G.add_node('Creator')
        for process in self._elements:
            G.add_node(str(process))
        G.add_node('Disposer')

        # adding edges
        def name_node(node: int, total: int):
            if node == 0:
                return 'Creator'
            elif node == total:
                return 'Disposer'
            else:
                return f'Process {node - 1}'

        G.add_edges_from(list(map(lambda x: (name_node(x[0], len(self._links)),
                                             name_node(x[1], len(self._links))),
                                  self._links)))

        # returns graph
        return G

    def _connect_scheme(self) -> NoReturn:
        """
        Connects the scheme elements
        :return:
        """

