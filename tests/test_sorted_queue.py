from unittest import TestCase

from app.models import SortedQueue


class TestSortedQueue(TestCase):

    def setUp(self) -> None:
        self.queue = SortedQueue()

    def test_insert(self):
        self.queue.insert(5)
        self.assertEqual(1, len(self.queue))

    def test_get(self):
        self.queue.insert(5)
        value = self.queue.get()
        self.assertEqual(5, value)
        self.assertEqual(0, len(self.queue))

    def test_update(self):
        self.queue.update([3, 2, 1])
        value = self.queue.get()
        self.assertEqual(1, value)
        self.assertEqual(2, len(self.queue))