import networkx as nx
from vehicle import vehicle

class Scheduling():

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
        
    def find_assign_trip(s, e, heuristic):
        """
        Assigns best available vehicle manage a certain trip. Returns False if no vehicles are available.

        Parameters: (self, p)
            s - (lat, lon)
            e - (lat, lon)
            heuristic - Callable()
        """
        times = [(v.distance_to(self.graph, s, heuristic), v) for v in self.vehicles]
        m = min(times)
        if m[0] != "inf":
            m[1].assign_trip(G, s, e, heuristic)
            self.log[v] = self.log.get(v, []) + [(s, e)]
        else:
            return False