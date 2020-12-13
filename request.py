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
        """ 
        Returns whether the Request is selected.
        """
        return self.selected

    def get_seats(self):
        """ 
        Returns the number of seats.
        """
        return self.seats

    def get_time(self):
        """ 
        Returns the maximum time.
        """
        return self.max_time

    def get_pickup_time(self):
        """ 
        Returns the pickup time.
        """
        return self.pickup_time

    def stop(self):
        """ 
        Returns the final location.
        """
        return self.stop

    def start(self):
        """ 
        Returns the starting location.
        """
        return self.start

    def select(self):
        """ 
        Selects the Request.
        """
        self.selected = True

    def rush(self):
        self.rush = True

    def night(self):
        self.night = True

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