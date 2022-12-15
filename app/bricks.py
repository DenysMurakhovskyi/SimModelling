import logging
from random import randint
from typing import Union

from .models import Element, Entity, Operation


class Creator(Element):

    def process(self):
        if self._parent.parent.check_creation_moment():
            logging.info(f'Created: {(entity := Entity(creation_time=self._parent.parent.timer))}')
            self._put_in_successor_queue(entity)


class Process(Element):

    def __init__(self, number, queue_size, parent=None):
        super().__init__(queue_size=queue_size)
        self.processing_entity: Union[None, Entity] = None
        self.process_finish_time: int = 0
        self._number = number
        self._parent = parent

    def __repr__(self):
        return f'Process {self._number}'

    def __str__(self):
        return f'Process {self._number}'

    def put_in_queue(self, entity: Entity):
        if self.processing_entity is None:
            self._start_process(entity)
        else:
            if self.queue.qsize() < self.queue.maxsize:
                self.queue.put(entity)
                logging.debug(f'The entity {entity} was put in queue of {self}')
            else:
                logging.debug(f'The entity {entity} was dropped')

    def _start_process(self, entity: Entity):
        self.processing_entity = entity
        self.process_finish_time = self._parent.parent.timer + (duration := randint(
            self._parent.time_processing_interval[0],
            self._parent.time_processing_interval[1]))
        self._parent.parent.add_moment(self.process_finish_time)
        logging.debug(f'In {self} the {entity} is processed from {self._parent.parent.timer}'
                      f' till {self.process_finish_time}')
        stats = Operation(start=self._parent.parent.timer,
                          duration=duration,
                          entity=entity,
                          processor=self,
                          operation_type='process')
        self._parent.parent.add_stats(stats)

    def process(self):
        if (self._parent.parent.timer == self.process_finish_time) and (self.processing_entity is not None):
            self._put_in_successor_queue(self.processing_entity)
            if not self.empty_queue:
                self._start_process(self._queue.get())
                pass


class Disposer(Element):

    def put_in_queue(self, entity: Entity):
        logging.info(f'{entity} was disposed at {self._parent.parent.timer}')
