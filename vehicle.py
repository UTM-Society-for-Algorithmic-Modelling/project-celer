from astar import diste, print_trip_info, find_closest_node, draw_graph, distance_to_meters
import networkx as nx
import math
import matplotlib.pyplot as plt
from datetime import timedelta, datetime
from request import Request
import numpy as np

class Vehicle():
    """
    Represents a vehicle.

    ===Attributes===
    position: (lat, lon)
    maximum_speed: max speed of the vehicle in m/s
    fuel: km remaining before charge/refuel
    current_speed: current speed of the vehicle in m/s
    acceleration: current acceleration fo the vehicle in m/s^2
    angle: angle the vehicle is pointing in
    available: if the vehicle is available for a trip
    seats: the number of seats in the vehicle
    trips: list of trip dictionaries (keys: "starting", "ending", "path")
    id: number representing the vehicle
    """
    position: tuple
    maximum_speed: int
    fuel: int
    current_speed: int
    acceleration: float
    angle: float
    available: bool
    seats: int
    trips: list
    log: list
    temp_path: list
    id: int

    def __init__(self, position, maximum_speed, fuel, current_speed, available, seats, id=0):
        self.position = position
        self.maximum_speed = maximum_speed
        self.fuel = fuel
        self.current_speed = current_speed
        self.acceleration = 3.5 # m/s^2
        self.angle = 0
        self.available = available
        self.seats = seats
        self.trips = []
        self.log = []
        self.temp_path = []
        self.id = id

    def is_available(self):
        """
        Return self.available.
        """
        return self.available

    def seat_number(self):
        """
        Return self.seats.
        """
        return self.seats

    def distance_to(self, G, p, heuristic):
        """
        Return the distance from self.position to p in estimated time of trip (min). Returns inf if vehicle is unavailable.

        Parameters: (self, G, p, heuristic)
            G - networkx.graph()
            p - (lat, lon)
            heuristic - callable
        """
        if self.available and distance_to_meters(self.position, p) < 3000:
            closest_intersection_to_pos = find_closest_node(G, self.position)
            closest_intersection_to_p = find_closest_node(G, p)
            try:
                path = nx.astar_path(G, closest_intersection_to_pos, closest_intersection_to_p, heuristic)
                return print_trip_info(closest_intersection_to_pos, closest_intersection_to_p, path, G)[2]
            except:
                print("No path")
        return float("inf")

    def assign_trip(self, G, trip, heuristic):
        """
        Assign a trip to this vehicle.

        Parameters: (self, G, starting, ending, heursitic)
            G - networkx.graph()
            trip - Request()
            heuristic - callable
        """
        starting = trip.start
        ending = trip.stop
        time = trip.pickup_time
        closest_intersection_to_pos = find_closest_node(G, self.position)
        closest_intersection_to_starting = find_closest_node(G, starting)
        closest_intersection_to_ending = find_closest_node(G, ending)
        trip = {"starting": starting, "ending": ending, "start_time": time, "end_time": time, "path": nx.astar_path(G, closest_intersection_to_pos, closest_intersection_to_starting, heuristic)[:-1] + nx.astar_path(G, closest_intersection_to_starting, closest_intersection_to_ending, heuristic)}
        self.trips.append(trip)
        print_trip_info(closest_intersection_to_pos, closest_intersection_to_ending, self.trips[0]["path"], G)
        self.available = False
        if self.temp_path is not None:
            self.temp_path.append(trip["path"].copy())

    def complete_trip(self):
        """
        Finished the first trip in self.trips

        Parameters: (self)
        """
        self.available = True
        if self.trips:
            self.log.append(self.trips[0])
            self.log[-1]["path"] = self.temp_path[0]
            self.temp_path.pop(0)
            self.trips.pop(0)
        if self.fuel < 50:
            pass
            # Find place to refuel and setup trip

    def move(self, G, s=1):
        """
        Moves the vehicle s seconds.

        Parameters: (self, G, s)
            G - networkx.graph()
            s - float
        """
        # Idea: travel as many full edges as we can and then do part of one edge.
        if not len(self.trips):
            return
        if self.trips[0]["end_time"] is not None:
            self.trips[0]["end_time"] += timedelta(seconds=s)
        can_move = s
        current = 1
        nodes = len(self.trips[0]["path"])
        # Go as far from node to node as possible with only full edges
        while current < nodes:        
            dist = np.divide(abs(distance_to_meters(self.position, self.trips[0]["path"][current])),(G[self.trips[0]["path"][current-1]][self.trips[0]["path"][current]]["speed"]))
            if can_move >= dist:
                can_move = np.subtract(can_move,dist)
            else:
                break
            self.position = self.trips[0]["path"][current]
            current += 1
        if current == nodes:
            self.position = self.trips[0]["path"][-1]
            self.complete_trip()
            return
        # Remove nodes we just traveled
        for i in range(current-1):
            self.trips[0]["path"].pop(0)
        # Travel part of of edge but not full
        to = self.trips[0]["path"][1] 
        # Get x and y distance in meters
        x_dif = np.int64(np.multiply(abs(distance_to_meters((self.position[0], 0), (to[0], 0))), 10**15))		         
        y_dif = np.int64(np.multiply(abs(distance_to_meters((0, self.position[1]), (0, to[1]))),10**15))
        if x_dif == 0: # Adjacent side has no length so the angle is either +-pi/2
            if np.subtract(np.int64(np.multiply(to[0],10**15)),np.int64(np.multiply(self.position[0],10**15))) > 0:
                self.angle = math.pi / 2
            if np.subtract(np.int64(to[0]*10**15), np.int64(self.position[0]*10**15)) < np.int64(0):
                self.angle = np.multiply(np.int64(-1*10**15), np.divide(np.pi, 2))

            # Main focus could totally change dir - if angle is too small we could point the opposite way due to catastrophic cancellation
        else:
            temp = np.divide(y_dif, x_dif)
            self.angle = np.arctan(np.absolute(temp))
            # Adjust angle based on wether x and y are +/-
            if np.subtract(np.int64(to[0]*10**15), np.int64(self.position[0]*10**15)) < np.int64(0):
                if np.subtract(np.int64(to[1]*10**15), np.int64(self.position[1]*10**15)) > np.int64(0):
                    self.angle = np.add(self.angle, np.divide(np.pi,2))
                else:
                    self.angle = np.add(self.angle, np.pi)
            else:
                if np.subtract(np.int64(to[1]*10**15), np.int64(self.position[1]*10**15)) < np.int64(0):
                        self.angle = np.subtract(self.angle, np.divide(np.pi, 2))
        # Move at the correct angle
        x_move = np.int64(can_move*10**15) * np.cos(self.angle) * G[self.trips[0]["path"][0]][self.trips[0]["path"][1]]["speed"]
        y_move = np.int64(can_move*10**15) * np.sin(self.angle) * G[self.trips[0]["path"][0]][self.trips[0]["path"][1]]["speed"]
        if  np.int64(0) <= np.subtract(np.absolute(x_move), np.absolute(x_dif)) or np.int64(0) <= np.subtract(np.absolute(y_move), np.absolute(y_dif)):
            self.position = to
        else:
            lat_per_1d = 111000
            lon_per_1d = np.multiply(np.cos(self.position[0]),111321)
            if abs(np.subtract(np.multiply(to[0],10**15),np.multiply(self.position[0],10**15))) <= abs(np.divide(x_move,lat_per_1d)) or abs(np.subtract(np.multiply(to[1],10**15),np.multiply(self.position[1],10**15))) <= abs(np.divide(y_move,lon_per_1d)):
                self.position = to
            else:
                self.position = np.divide(np.add(np.multiply(self.position[0],10**15), np.divide(x_move,lat_per_1d)),10**15), np.divide(np.add(np.multiply(self.position[1],10**15), np.divide(y_move,lon_per_1d)),10**15)
        if self.position == to:
            self.trips[0]["path"].pop(0)
            if len(self.trips[0]["path"]) == 1:
                self.complete_trip()

    def __eq__(self, other):
        return self


    def __repr__(self):
        s = f"=== Vehicle ID - {self.id} ===\n"
        if self.log != []:
            s += "Log -"
            for l in self.log:
                temp = ""
                for dn, d in l.items():
                    if dn != "path":
                        temp += f"\t{dn} - {d}\n"
                s += temp + "\n"
        else:
            s += "No Trips in this Round"
        return  s


# === Main - An example test ===
if __name__ == "__main__":
    from astar import load_data
    G, trips = load_data(reset=False, graph=False, trip=False, abbr=False)
    plt.ion()

    v1 = Vehicle((40.74345679662331, -73.72770035929027), 200.0, 10.0, 20.0, True, 4) # Creates our Vehicle
    draw_graph(G, bounds=((40.74345679662331, -73.72770035929027), (40.77214782804362, -73.76426798716528))) # Draws the graph
    v1.assign_trip(G, Request((40.74345679662331, -73.72770035929027), (40.77214782804362, -73.76426798716528), 0, 0, datetime(2015,1,1)), diste) # Assigns a trip to our Vehicle
    
    # Moves our vehicle based on the move function
    total = 0
    while not v1.available:
        v1.move(G,2)
        plt.plot([v1.position[1]], [v1.position[0]], "mo")
        plt.draw()
        total+=1
        print("Seconds: " + str(total))
        plt.pause(0.000001)
    plt.show()
    plt.pause(5)