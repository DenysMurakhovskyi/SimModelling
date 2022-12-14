from typing import Union

from .models import Element, Entity


class Creator(Element):
    pass


class Process(Element):

    def __init__(self, number):
        super().__init__()
        self.processing_entity: Union[None, Entity] = None
        self.process_finish_time: int = 0
        self._number = number

    def __repr__(self):
        return f'Process {self._number}'

    def __str__(self):
        return f'Process {self._number}'


class Disposer(Element):
    pass