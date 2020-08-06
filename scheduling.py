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
        s = trip[0]
        e = trip[1]
        times = [(v.distance_to(self.graph, s, heuristic), v) for v in self.vehicles]
        m = min(times)
        if m[0] != "inf":
            m[1].assign_trip(self.graph, trip, heuristic)
            self.log[m[1].id] = self.log.get(m[1].id, []) + [(trip)]
            return True
        else:
            return False
        
    def move(self):
        """
        Moves all vehicles in self.vehicles.

        Parameters: (self)
        """
        for vehicle in self.vehicles:
            vehicle.move(self.graph)