import networkx as nx
from vehicle import Vehicle
from admission_control import admission_control

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
        Assigns best available vehicle manage a certain trips. Return True if trip-vehicle
        pair was assigned, False otherwise.

        Parameters: (self, trip, heuristic)
            trips - Request()
            heuristic - Callable()
        """
        ac = admission_control(trip, self.vehicles, self.graph) # {vehicle ID: request()}
        for v in self.vehicles:
            if v.id in ac.keys():
                v.assign_trip(self.graph, ac[v.id], heuristic)
                return True
        return False
        # Note: AC key will be -1 if this request is not possible/no profit/no cars
        
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
