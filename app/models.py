from abc import ABC
from dataclasses import dataclass
from queue import Queue
from typing import Literal, List
from uuid import uuid4


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

    def process(self):
        pass

    def put_into_output(self):
        pass





