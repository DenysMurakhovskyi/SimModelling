from typing import List, Tuple, NoReturn, Union
import networkx as nx
import matplotlib.pyplot as plt
from queue import Queue

from .bricks import Creator, Process, Disposer

DEFAULT_QUEUE_SIZE = 5


class SimulationScheme:

    def __init__(self, links: List[Tuple],
                 queue_len: Union[List[int], int, None] = None,
                 number_of_processes: int = 1):
        # inputs check
        if len(links) < number_of_processes + 1:
            raise ValueError(f'The _scheme is not properly connected. Links:{len(links)}, '
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

    @property
    def all_elements(self):
        return sum([[self._start_point], self._elements, [self._end_point]], [])

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
            scheme_object = self.all_elements[link[0]]
            scheme_queue = self.all_elements[link[1]].queue

            if scheme_object.outputs is None:
                scheme_object.outputs = scheme_queue
            elif isinstance(scheme_object.outputs, Queue):
                temp_queue = scheme_object.outputs
                scheme_object.outputs = [temp_queue, scheme_queue]
            elif isinstance(scheme_object.outputs, list):
                scheme_object.outputs.append(scheme_queue)
            else:
                raise TypeError(f"Error in outputs of {self}")
