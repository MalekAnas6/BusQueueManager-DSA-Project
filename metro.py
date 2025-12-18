# Node Class
class WagonNode:
    # Constructor
    def __init__(self, wagon_id, capacity):
        self.wagon_id = wagon_id
        self.capacity = capacity
        self.passengers = 0
        self.next = None

# Linked List class
class Metro:
    # Constructor
    def __init__(self, metro_id):
        self.metro_id = metro_id
        self.head = None 
        self.wagon_count = 0

    # Add Function
    def add_wagon(self, wagon_id, capacity):
        new_wagon = WagonNode(wagon_id, capacity)
        
        # Check if list is empty (Head)
        # First Node ---
        if self.head is None:
            self.head = new_wagon
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_wagon
            
        self.wagon_count += 1
        return True

    # Delete Function
    def delete_last_wagon(self):
        # Check if empty
        if self.head is None:
            return False

        # Single node case
        if self.head.next is None:
            self.head = None
        else:
            # 
            current = self.head
            while current.next.next is not None:
                current = current.next
            current.next = None
            
        self.wagon_count -= 1
        return True

    # Send Data to UI Function
    def get_metro_data(self):
        wagons_list = []
        current = self.head
        while current is not None:
            wagons_list.append({
                "id": current.wagon_id,
                "capacity": current.capacity,
                "passengers": current.passengers
            })
            current = current.next
        return wagons_list