import networkx as nx
from vehicle import Vehicle

class Scheduling():
    """
    The schdeuling algorithm.

    ===Attributes===
    vehicles: list of all vehicles being controlled by the celer system
    graph: graph representing the map
    log: dictionary with all trips and who got them
    """
    vehicles: list
    graph: dict
    log: dict

    def __init__(self, G):
        self.vehicles = []
        self.graph = G
        self.log = {}

    def add_vehicle(self, v):
        """
        Adds a vehicle.

        Parameters: (self, v)
            v - Vehicle()
        """
        self.vehicles.append(v)
        
    def find_assign_trip(self, trip, heuristic):
        """
        Assigns best available vehicle manage a certain trip. Returns False if no vehicles are available.

        Parameters: (self, trip, heuristic)
            trip - trip
            heuristic - Callable()
        """
        s = trip["starting_pos"]
        e = trip["ending_pos"]
        times = [(v.distance_to(self.graph, s, heuristic), v) for v in self.vehicles]
        m = min(times)
        if m[0] != "inf":
            m[1].assign_trip(self.graph, trip, heuristic)
            return True
        else:
            return False
        
    def move(self, s=1):
        """
        Moves all vehicles in self.vehicles, s seconds.

        Parameters: (self, s)
            s - float
        """
        for vehicle in self.vehicles:
            vehicle.move(self.graph, s)

    def get_logs(self):
        """
        Creates and returns logs for all vehicles.
        """
        for v in self.vehicles:
            self.log[v.id] = self.log.get(v.id, []) + v.log
        return self.log