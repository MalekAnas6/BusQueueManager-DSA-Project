from metro import Metro
from metro_queue import MetroQueue

class MetroManager:
   
    def __init__(self):
        
        self.metro = Metro(metro_id=1)
        self.queue = MetroQueue()

    def add_wagon(self, wagon_id, capacity):
        return self.metro.add_wagon(wagon_id, capacity)

    def remove_last_wagon(self):
        return self.metro.delete_last_wagon()

    def add_passenger(self, passenger_name, priority):
        self.queue.enqueue(passenger_name, priority)

    def board_passenger(self):
        if self.queue.is_empty():
            return False

        current_wagon = self.metro.head
        passenger_boarded = False

        while current_wagon is not None:
            if current_wagon.passengers < current_wagon.capacity:
                
                passenger_name = self.queue.dequeue()
                
                if passenger_name:
                    current_wagon.passengers += 1
                    passenger_boarded = True
                    
                break 
            current_wagon = current_wagon.next

        return passenger_boarded

    def get_metro_data(self):
        return self.metro.get_metro_data()

    def get_queue_data(self):
        return self.queue.get_all_passengers()
