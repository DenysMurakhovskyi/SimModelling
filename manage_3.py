from app.scheme import SimulationScheme
from app.simulator import Simulation


if __name__ == '__main__':

    simulation_scheme = SimulationScheme(links=[(0, 1), (0, 2), (0, 3), (1, 4), (2, 4), (3, 4)],
                                         number_of_processes=3,
                                         time_creation_interval=(1, 5),
                                         time_processing_interval=(10, 20))
    simulation_scheme.compile()

    simulation = Simulation(time_period=100,
                            scheme=simulation_scheme)
    simulation.run()
    simulation.show_all_processor_stats()
