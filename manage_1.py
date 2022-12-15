from app.scheme import SimulationScheme
from app.simulator import Simulation


if __name__ == '__main__':

    simulation_scheme = SimulationScheme(links=[(0, 1), (1, 2)],
                                         number_of_processes=1,
                                         time_creation_interval=(2, 4),
                                         time_processing_interval=(1, 2))
    simulation_scheme.compile()

    simulation = Simulation(time_period=100,
                            scheme=simulation_scheme)
    simulation.run()
    simulation.show_processor_stats(0)
