from .bus import Bus
from .queue import Queue

class Manager:
    def __init__(self):
        self.buses = []
        self.waiting_queue = Queue()
    
    def add_bus(self, bus_ID, capacity):
        new_bus = Bus(bus_ID, capacity)
        self.buses.append(new_bus)
    
    def get_buses_status(self):
        return [bus.get_status() for bus in self.buses]
    
    def add_passenger_to_queue(self, passenger_name):
        return self.waiting_queue.enqueue(passenger_name)
    
    def get_queue_status(self):
        return self.waiting_queue.get_size()
    
    def board_passenger(self):
        logs = []
        for bus in self.buses:
            while not bus.is_full() and not self.waiting_queue.is_empty():
                passenger = self.waiting_queue.dequeue()
                if bus.load_passenger(passenger):
                    logs.append(f"Passenger {passenger} boarded Bus {bus.bus_ID}.")
                else:
                    self.waiting_queue.enqueue(passenger)
                    break
        return logs
    
    def unload_passenger(self, passenger_name):
        logs = []
        for bus in self.buses:
            if bus.unload_passenger(passenger_name):
                logs.append(f"Passenger {passenger_name} unloaded from Bus {bus.bus_ID}.")
                break
        return logs
