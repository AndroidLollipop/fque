import math
import queue


class LimitedSimpleQueue(queue.SimpleQueue):
    def __init__(self, maxsize: int = 0):
        super().__init__()
        self.__maxsize = maxsize if maxsize > 0 else math.inf

    def put(self, item):
        # rigorous size limiting cannot be achieved without synchronization
        # however, the amount by which qsize can exceed maxsize is bounded
        if self.qsize() > self.__maxsize:
            raise queue.Full
        return super().put(item)
