"""
Compares the performance of
- fque.Queue
- queue.Queue
"""
import threading
import time

import queue
import fque


class Producer(threading.Thread):
    _queue = None

    def __init__(self, iters=100):
        self.pending = iters
        super().__init__()

    def assign_queue(self, q):
        self._queue = q

    def work(self):
        self._queue.put(self.produce())

    def produce(self):
        return 100

    def run(self):
        while self.pending > 0:
            self.pending -= 1
            self.work()


class Consumer(threading.Thread):
    _queue = None

    def __init__(self):
        super().__init__(daemon=True)

    def assign_queue(self, q):
        self._queue = q

    def work(self):
        return self._queue.get()

    def run(self):
        while True > 0:
            self.work()


def measure_performance(producers: int, consumers: int, q):
    n = 50_000  # Messages per producer
    prods = [Producer(iters=n) for i in range(producers)]
    cons = [Consumer() for i in range(consumers)]
    start = time.time()
    for worker in prods + cons:
        worker.assign_queue(q)
        worker.start()
    for worker in prods:
        worker.join()
    while not q.empty():
        time.sleep(0.01)
    duration = time.time() - start
    return duration


if __name__ == '__main__':
    # Producing faster than consuming
    nq = queue.Queue(maxsize=0)
    fq = fque.Queue(maxsize=0)
    n_duration = measure_performance(5, 1, nq)
    f_duration = measure_performance(5, 1, fq)
    print('        | Queue   | Fque    ')
    print('{:<8}| {:<8}| {:<8}'.format('5p-1c', round(n_duration, 2), round(f_duration, 2)))

    # Consuming at same speed than producing
    nq = queue.Queue(maxsize=0)
    fq = fque.Queue(maxsize=0)
    n_duration = measure_performance(5, 5, nq)
    f_duration = measure_performance(5, 5, fq)
    print('{:<8}| {:<8}| {:<8}'.format('5p-5c', round(n_duration, 2), round(f_duration, 2)))

    # Consuming faster than producing
    nq = queue.Queue(maxsize=0)
    fq = fque.Queue(maxsize=0)
    n_duration = measure_performance(1, 5, nq)
    f_duration = measure_performance(1, 5, fq)
    print('{:<8}| {:<8}| {:<8}'.format('1p-5c', round(n_duration, 2), round(f_duration, 2)))



