class Bus:
    def __init__(self, bus_ID, capacity):
        self.bus_ID = bus_ID
        self.capacity = capacity
        self.passengers = []

    def is_full(self):
        return len(self.passengers) >= self.capacity

    def load_passenger(self, name):
        if not self.is_full():
            self.passengers.append(name)
            return True
        else:
            return False
        

    def unload_passenger(self, name):
        if name in self.passengers:
            self.passengers.remove(name)
            return True
        else:
            return False
        
    def get_status(self):
        return {
            "Bus ID": self.bus_ID,
            "Capacity": self.capacity,
            "Current Passengers": len(self.passengers),
            "Remaining Seats": self.capacity - len(self.passengers),
            "Passengers": self.passengers
        }
    

    def __repr__(self):
        return f"Bus({self.bus_ID}, {self.capacity}, {self.passengers})"
        
