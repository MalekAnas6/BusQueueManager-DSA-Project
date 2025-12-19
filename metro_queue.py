from collections import deque
import heapq

class MetroQueue:
    def __init__(self):
        self.pq = []
        self.counter = 0

    def enqueue(self, passenger_name, priority=10):
        heapq.heappush(self.pq, (priority, self.counter, passenger_name))
        self.counter += 1

    def dequeue(self):
        if not self.is_empty():
            priority, _, passenger_name = heapq.heappop(self.pq)
            return passenger_name
        return None

    def peek(self):
        if not self.is_empty():
            return self.pq[0][2]
        return None

    def is_empty(self):
        return len(self.pq) == 0

    def size(self):
        return len(self.pq)

    def get_all_passengers(self):
        return [item[2] for item in sorted(self.pq)]
