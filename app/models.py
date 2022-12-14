from abc import ABC
from dataclasses import dataclass
from queue import Queue
from typing import Literal, List, NoReturn, Any, Iterable
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

    operations: List[Operation]


class Element(ABC):

    def __init__(self, queue_size=0,
                 outputs=None):
        if queue_size == -1:
            self._queue = None
        else:
            self._queue = Queue(maxsize=queue_size)

        self.outputs = outputs
        self._uid = uuid4()

    @property
    def element_id(self):
        return self._uid

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







