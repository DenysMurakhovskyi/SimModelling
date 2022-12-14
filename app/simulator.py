from .scheme import SimulationScheme
from typing import List, Tuple, Union
from .models import SortedQueue
from random import randint


class Simulation:
    """
    The class which executes a simulation using the simulation _scheme and other parameters set
    """

    def __init__(self, time_period: int,
                 scheme: SimulationScheme,
                 time_interval: Tuple[int, int]):

        self._time_period = time_period
        self._scheme = scheme
        self._time_interval = time_interval
        self._creation_moments: List[int] = []
        self._moments_list: SortedQueue = SortedQueue()
        self._current_time = 0

    @property
    def timer(self):
        return self._current_time

    def run(self):
        self._creation_moments = self._generate_creations_list()
        self._moments_list.update(self._creation_moments)

        self._current_time = self._moments_list.get()

        while self._current_time < self._time_period:
            # main simulation loop



            # timer update
            next_time = self._moments_list.get()
            if next_time < self._time_period:
                self._current_time = next_time
            else:
                self._current_time = self._time_period


    def _generate_creations_list(self) -> List[int]:
        timer, moments_list = 0, []
        while timer < self._time_period:
            moments_list.append(timer := timer + randint(self._time_interval[0],
                                                         self._time_interval[1]))
        return moments_list
