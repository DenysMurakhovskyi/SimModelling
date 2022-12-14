from typing import Union

from .models import Element, Entity


class Creator(Element):
    pass


class Process(Element):

    def __init__(self):
        super().__init__()
        self.processing_entity: Union[None, Entity] = None
        self.process_finish_time: int = 0


class Disposer(Element):
    pass