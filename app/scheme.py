from typing import List, Tuple, NoReturn, Union
import networkx as nx
import matplotlib.pyplot as plt
from queue import Queue

from .bricks import Creator, Process, Disposer

DEFAULT_QUEUE_SIZE = 5
DEFAULT_CREATION_INTERVAL = (1, 3)
DEFAULT_PROCESSING_INTERVAL = (5, 10)


class SimulationScheme:

    def __init__(self, links: List[Tuple],
                 queue_len: Union[List[int], int, None] = None,
                 number_of_processes: int = 1,
                 time_creation_interval=DEFAULT_CREATION_INTERVAL,
                 time_processing_interval=DEFAULT_PROCESSING_INTERVAL
                 ):
        # inputs check
        if len(links) < number_of_processes + 1:
            raise ValueError(f'The scheme is not properly connected. Links:{len(links)}, '
                             f'process: {number_of_processes}')

        if number_of_processes <= 0:
            raise ValueError('Number of processes should be a positive value')

        self._start_point: Creator = Creator(parent=self)
        self._end_point: Disposer = Disposer(parent=self)
        if not queue_len:
            queue_len = DEFAULT_QUEUE_SIZE
        if isinstance(queue_len, int):
            self._elements: List[Process] = [Process(n, queue_size=queue_len, parent=self)
                                             for n in range(number_of_processes)]
        elif isinstance(queue_len, list):
            self._elements: List[Process] = [Process(n, queue_size=current_queue_len, parent=self)
                                             for current_queue_len, n in zip(queue_len,
                                                                             list(range(number_of_processes)))]
        else:
            raise TypeError('Illegal type for queue length')

        self._links = links
        self._compiled = False
        self._parent = None
        self.time_creation_interval = time_creation_interval
        self.time_processing_interval = time_processing_interval

    @property
    def all_elements(self):
        return sum([[self._start_point], self._elements, [self._end_point]], [])

    @property
    def creator(self):
        return self._start_point

    @property
    def disposer(self):
        return self._end_point

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def processes(self):
        return self._elements

    def compile(self):
        self._connect_scheme()
        self._compiled = True

    def show_scheme(self) -> NoReturn:
        """
        Represents the _scheme as a directed graph
        """
        if not self._compiled:
            raise RuntimeError('The scheme is not compiled')

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
        for link in self._links:
            if link[1] == 0:
                raise RuntimeError('The Creator does not have an input')

            scheme_output = self.all_elements[link[0]]
            scheme_input = self.all_elements[link[1]]

            if scheme_output.successor is None:
                scheme_output.successor = scheme_input
            elif isinstance(scheme_output.successor, Queue):
                scheme_output.outputs = [scheme_output.successor, scheme_input]
            elif isinstance(scheme_output.successor, list):
                scheme_output.successor.append(scheme_input)
            else:
                raise TypeError(f"Error in outputs of {self}")
