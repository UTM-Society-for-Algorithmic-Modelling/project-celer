class Request():
    """
    Represents a trip request by the user/system.
    
    ===Attributes===
    start: (lat, long)
    stop: (lat, long)
    max_time: int
    seats: int
    pickup_time: datetime
    selected: bool
    """
    
    def __init__(self, start, stop, max_time, seats, pickup_time):
        self.start = start
        self.stop = stop
        self.max_time = max_time
        self.seats = seats
        self.pickup_time = pickup_time
        self.selected = False
        self.rush = False
        self.night = False

    def is_selected(self):
        return self.selected

    def get_seats(self):
        return self.seats

    def get_time(self):
        return self.max_time

    def get_pickup_time(self):
        return self.pickup_time

    def stop(self):
        return self.stop

    def start(self):
        return self.start

    def select(self):
        self.selected = True

    def rush(self):
        self.rush = True # Methods available to extend this simulation in the future

    def night(self):
        self.night = True # # Methods available to extend this simulation in the future

    def is_rush(self):
        return self.rush

    def is_night(self):
        return self.night

    def __lt__(self, other):
        return self.pickup_time < other.pickup_time

    def __eq__(self, other):
        return self.pickup_time == other.pickup_time

    def __gt__(self, other):
        return self.pickup_time > other.pickup_time

    def __repr__(self):
        s = f"=== Request ===\nStart - {self.start}\nStop - {self.stop}\nPickup Time - {self.pickup_time}\n"
        return  s
