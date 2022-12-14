from abc import ABC
from dataclasses import dataclass
from queue import Queue
from typing import Literal, List, NoReturn, Any, Iterable, Union
from uuid import uuid4
from sortedcontainers import SortedList


@dataclass
class Entity:
    """
    Represents an entity in the system
    """

    uid: str
    creation_time: int
    disposal_time: int


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


@dataclass
class Statistics:
    """
    Gathers statistics and make some reports
    """

    _operations: List[Operation]

    def save(self, value: Operation) -> NoReturn:
        self._operations.append(value)


class Element(ABC):

    def __init__(self, queue_size: int = 0,
                 parent: Any = None):

        if queue_size == -1:
            self._queue = None
        else:
            self._queue = MarkedQueue(maxsize=queue_size, parent=self)

        self._parent = parent
        self.outputs: Union[Queue, List[Queue], None] = None
        self._uid = uuid4()

    def __repr__(self):
        return self.__class__.__name__

    @property
    def element_id(self):
        return self._uid

    @property
    def queue(self):
        return self._queue

    def process(self, moment_of_time: int):
        pass


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


class MarkedQueue(Queue):

    def __init__(self, maxsize, parent=None):
        super().__init__(maxsize=maxsize)
        self._parent = parent

    def __repr__(self):
        return f'Queue (size: {self.qsize()}) of {self._parent}'

