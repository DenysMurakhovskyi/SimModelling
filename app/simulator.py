from .scheme import SimulationScheme
from typing import List, Tuple, Union
from sortedcontainers import SortedList
from random import randint


class Simulation:
    """
    The class which executes a simulation using the simulation scheme and other parameters set
    """

    def __init__(self, time_period: int,
                 scheme: SimulationScheme,
                 time_interval: Tuple[int, int]):
        self.time_period = time_period
        self.scheme = scheme
        self.time_interval = time_interval
        self.creation_moments: List[int] = self._generate_creations_list()
        self.moments_list: SortedList = SortedList()
        self.moments_list.update(self.creation_moments)

    def _generate_creations_list(self) -> List[int]:
        timer, moments_list = 0, []
        while timer < self.time_period:
            moments_list.append(timer := timer + randint(self.time_interval[0],
                                                         self.time_interval[1]))
        return moments_list
