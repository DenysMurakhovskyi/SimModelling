from unittest import TestCase, skip

from app.scheme import SimulationScheme


class TestSimulationScheme(TestCase):
    NUMBER_OF_ELEMENTS_EASY = 1
    NUMBER_OF_ELEMENTS_TASK = 5
    NUMBER_OF_ELEMENTS_ADVANCED = 7

    def test_exceptions(self):
        with self.assertRaises(ValueError):
            SimulationScheme(links=[(0, 1), (1, 2)],
                             number_of_processes=0)

        with self.assertRaises(ValueError):
            SimulationScheme(links=[(0, 1)],
                             number_of_processes=1)

    def test_creation_easy(self):
        scheme = SimulationScheme(links=[(0, 1), (1, 2)],
                                  number_of_processes=self.NUMBER_OF_ELEMENTS_EASY)
        self.assertEqual(1, len(scheme.elements))
        self.assertEqual('Creator', scheme.start_point.__class__.__name__)
        self.assertEqual('Disposer', scheme.end_point.__class__.__name__)
        self.assertEqual('Process', scheme.elements[0].__class__.__name__)

    def test_graphing(self):
        scheme = SimulationScheme(links=[(0, 1), (1, 2)],
                                  number_of_processes=self.NUMBER_OF_ELEMENTS_EASY)
        scheme.show_scheme()

