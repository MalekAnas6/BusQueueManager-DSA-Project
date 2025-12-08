class Node :
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue :
    def __init__(self,max_size):
        self.front = None
        self.rear = None
        self.size = 0
        self.max_size = max_size
    
    def is_empty(self):
        return self.size == 0
    
    def is_full(self):
        return self.size == self.max_size
    
    def enqueue(self, data):
        if self.is_full():
            return False
        
        new_node = Node(data)
        
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            return None
        
        removed_data = self.front.data
        self.front = self.front.next
        
        if self.front is None:
            self.rear = None
        
        self.size -= 1
        return removed_data
    
    def peek(self):
        if self.is_empty():
            return None
        return self.front.data
    
    def get_size(self):
        items = []
        current = self.front
        while current:
            items.append(current.data)
            current = current.next
        return {
            "size": self.size,
            "items": items,
            "is_full": self.is_full(),   
            "is_empty": self.is_empty()
            }
    def __repr__(self):
        return f"Queue(size={self.size}, max_size={self.max_size} ,elements={self.get_size()['items']})"
