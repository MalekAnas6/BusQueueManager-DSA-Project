from collections import deque

class Queue:
    def __init__(self, max_size):
        self.queue = deque()
        self.max_size = max_size

    def is_empty(self):
        return len(self.queue) == 0

    def is_full(self):
        return len(self.queue) == self.max_size

    def enqueue(self, passenger):
        if self.is_full():
            return False
        self.queue.append(passenger)
        return True

    def dequeue(self):
        if self.is_empty():
            return None
        return self.queue.popleft()

    def peek(self):
        if self.is_empty():
            return None
        return self.queue[0]

    def get_size(self):
        return {
            "size": len(self.queue),
            "items": list(self.queue),
            "is_full": self.is_full(),
            "is_empty": self.is_empty()
        }