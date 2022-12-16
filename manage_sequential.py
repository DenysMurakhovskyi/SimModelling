from app.scheme import SimulationScheme
from app.simulator import Simulation


if __name__ == '__main__':

    simulation_scheme = SimulationScheme(links=[(0, 1), (1, 2), (2, 3), (3, 4)],
                                         number_of_processes=3,
                                         time_creation_interval=(100, 200),
                                         time_processing_interval=(50, 100))
    simulation_scheme.compile()
    simulation_scheme.show_scheme()

    simulation = Simulation(time_period=200,
                            scheme=simulation_scheme)
    simulation.run()
    simulation.show_all_processor_stats()