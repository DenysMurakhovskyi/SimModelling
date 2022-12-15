import logging
from random import randint, seed
from typing import List, NoReturn

from .models import SortedQueue, Statistics, Operation
from .scheme import SimulationScheme


class Simulation:
    """
    The class which executes a simulation using the simulation _scheme and other parameters set
    """

    def __init__(self, time_period: int,
                 scheme: SimulationScheme):

        self._time_period = time_period
        self._scheme = scheme
        self._scheme.parent = self
        self._time_interval = self._scheme.time_creation_interval
        self._creation_moments: List[int] = []
        self._moments_list: SortedQueue = SortedQueue()
        self._current_time = 0
        self._stat = Statistics()
        seed(101)

    @property
    def timer(self):
        return self._current_time

    def add_moment(self, time_value: int) -> NoReturn:
        if not self._moments_list.contains(time_value):
            self._moments_list.insert(time_value)

    def add_stats(self, operation: Operation) -> NoReturn:
        self._stat.save(operation)

    def check_creation_moment(self):
        return self._current_time in self._creation_moments

    def run(self):
        self._creation_moments = self._generate_creations_list()
        self._moments_list.update(self._creation_moments)

        self._current_time = self._moments_list.get()

        while self._current_time < self._time_period:
            logging.info(f'  === Time was shifted till {self.timer} time-interval ===')
            # main simulation loop

            for element in self._scheme.all_elements:
                logging.debug(f'Current processing element is {element}')
                element.process()

            # timer update
            next_time = self._moments_list.get()
            if next_time < self._time_period:
                self._current_time = next_time
            else:
                self._current_time = self._time_period

    def show_processor_stats(self, n: int) -> NoReturn:
        processor = self._scheme.processes[n]
        self._stat.show_single_element(processor)

    def _generate_creations_list(self) -> List[int]:
        timer, moments_list = 0, []
        while timer < self._time_period:
            moments_list.append(timer := timer + randint(self._time_interval[0],
                                                         self._time_interval[1]))
        return moments_list
