import logging
from abc import ABC
from dataclasses import dataclass, field
from queue import Queue
from typing import Literal, List, NoReturn, Any, Iterable, Union
from uuid import uuid1, UUID

from sortedcontainers import SortedList


@dataclass
class Entity:
    """
    Represents an entity in the system
    """

    uid: UUID = field(default_factory=uuid1)
    creation_time: int = -1
    disposal_time: int = -1

    def __repr__(self):
        return f'Entity with UUID {self.uid}(creation time is {self.creation_time})'

    def __str__(self):
        return f'Entity with UUID {self.uid}(creation time is {self.creation_time})'


@dataclass
class Operation:
    """
    Represents an operation on the entity in the defined processor
    """

    start: int
    duration: int
    entity: Entity
    processor: "Element"
    operation_type: Literal['put_in_queue', 'process', '']

    @property
    def stop(self):
        return self.start + self.duration


@dataclass
class Statistics:
    """
    Gathers statistics and make some reports
    """

    _operations: List[Operation] = field(default_factory=list)

    def save(self, value: Operation) -> NoReturn:
        self._operations.append(value)

    def show_single_element(self, element: "Element", upper_time_limit: int) -> NoReturn:
        duration = sum(list(map(lambda x: (x.stop if x.stop <= upper_time_limit else upper_time_limit) - x.start,
                                list(filter(lambda x: x.processor == element, self._operations)))))
        print(f'Loading time = {duration}')
        print(f'Relative loading time = {((duration / upper_time_limit) * 100):.2f} %')


class Element(ABC):

    def __init__(self, queue_size: int = 0,
                 parent: Any = None):

        if queue_size == -1:
            self._queue = None
        else:
            self._queue = MarkedQueue(maxsize=queue_size, parent=self)

        self._parent = parent
        self.successor: Union["Element", List["Element"], None] = None
        self._uid = uuid1()

    def __repr__(self):
        return self.__class__.__name__

    @property
    def element_id(self):
        return self._uid

    @property
    def empty_queue(self):
        if self._queue is None:
            return True
        else:
            return self._queue.qsize() == 0

    @property
    def queue(self):
        return self._queue

    @property
    def qsize(self):
        return self._queue.qsize()

    def process(self):
        pass

    def _get_successor(self):
        logging.debug("Choosing successor")
        if self.successor is None:
            return None
        elif isinstance(self.successor, Element):
            return self.successor
        elif isinstance(self.successor, list):
            # search for the shortest queue
            successor = self.successor[0]
            for element in self.successor:
                if successor.qsize == 0:
                    break
                if element.qsize < successor.qsize:
                    successor = element
            return successor

    def put_in_queue(self, entity: Entity):
        self._queue.put(entity)

    def _put_in_successor_queue(self, entity: Entity):
        if (value := self._get_successor()) is None:
            raise RuntimeError('The entity can not be put in None')
        else:
            value.put_in_queue(entity)


class SortedQueue:

    def __init__(self):
        self._list: SortedList = SortedList()

    def __len__(self):
        return len(self._list)

    def __repr__(self):
        return f'SortedList: {str(self._list)}'

    def insert(self, value: Any) -> NoReturn:
        self._list.add(value)

    def get(self) -> Any:
        value = self._list[0]
        self._list.pop(0)
        return value

    def update(self, list_of_values: Iterable) -> NoReturn:
        self._list.update(list_of_values)

    def contains(self, value):
        return value in self._list


class MarkedQueue(Queue):

    def __init__(self, maxsize, parent=None):
        super().__init__(maxsize=maxsize)
        self._parent = parent

    def __repr__(self):
        return f'Queue (size: {self.qsize()}) of {self._parent}'
