from unittest import TestCase
from app.simulator import Simulation
from app.scheme import SimulationScheme
import numpy as np


class TestSimulation(TestCase):

    NUMBER_OF_ELEMENTS_EASY = 1

    def setUp(self) -> None:
        self.simulation_scheme = SimulationScheme(links=[(0, 1), (1, 2)],
                                                  number_of_processes=self.NUMBER_OF_ELEMENTS_EASY)
        self.simulation = Simulation(time_period=1000,
                                     scheme=self.simulation_scheme,
                                     time_interval=(1, 5))

    def test_creation_interval(self):
        moments = self.simulation._generate_creations_list()
        self.assertIsNotNone(moments)

        moments = np.array(moments)
        delta_array = np.unique(moments.copy()[1:] - moments[:-1])
        self.assertLessEqual(np.max(delta_array), 5)
        self.assertLessEqual(1, np.min(delta_array))

    def test_run_simulation(self):
        self.simulation.run()
        self.assertLess(0, self.simulation.timer)
        self.assertLessEqual(self.simulation.timer, 1000)
