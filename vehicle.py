from astar import diste, print_trip_info, find_closest_node, draw_graph, distance_to_meters
import networkx as nx
import math
import matplotlib.pyplot as plt


class Vehicle():
    """
    Represents a vehicle.

    ===Attributes===
    position: (lat, lon)
    maximum_speed: max speed of the vehicle in km/h
    fuel: km remaining before charge/refuel
    current_speed: current speed of the vehicle in km/h
    available: if the vehicle is available for a trip
    seats: the number of seats in the vehicle
    trips: list of trip dictionaries (keys: "starting", "ending", "path")
    """
    position: tuple
    maximum_speed: int
    fuel: int
    current_speed: int
    available: bool
    seats: int
    trips: list

    def __init__(self, position, maximum_speed, fuel, current_speed, available, seats):
        self.position = position
        self.maximum_speed = maximum_speed
        self.fuel = fuel
        self.current_speed = current_speed
        self.acceleration = 3.5 # m/s^2
        self.angle = 0
        self.available = available
        self.seats = seats
        self.trips = []

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
        if self.available:
            closest_intersection_to_pos = find_closest_node(G, self.position)
            closest_intersection_to_p = find_closest_node(G, p)
            path = nx.astar_path(G, closest_intersection_to_pos, closest_intersection_to_p, heuristic)
            return print_trip_info(closest_intersection_to_pos, closest_intersection_to_p, path, G)[2]
        return float("inf")

    def assign_trip(self, G, starting, ending, heuristic):
        """
        Assign a trip to this vehicle.

        Parameters: (self, G, starting, ending, heursitic)
            G - networkx.graph()
            starting - (lat, lon)
            ending - (lat, lon)
            heuristic - callable
        """
        closest_intersection_to_pos = find_closest_node(G, self.position)
        closest_intersection_to_starting = find_closest_node(G, starting)
        closest_intersection_to_ending = find_closest_node(G, ending)
        trip = {"starting": starting, "ending": ending, "path": nx.astar_path(G, closest_intersection_to_pos, closest_intersection_to_starting, heuristic)[:-1] + nx.astar_path(G, closest_intersection_to_starting, closest_intersection_to_ending, heuristic)}
        self.trips.append(trip)
        print_trip_info(closest_intersection_to_pos, closest_intersection_to_ending, self.trips[0]["path"], G)
        self.available = False

    def complete_trip(self):
        """
        Finished the first trip in self.trips

        Parameters: (self)
        """
        self.available = True
        if self.trips:
            self.trips.pop(0)
        if self.fuel < 50:
            pass
            # Find place to refuel and setup trip

    def move(self, G):
        #self.current_speed += self.acceleration
        # Idea: travel as many full edges as we can and then do part of one edge.
        can_move = self.current_speed
        current = 1
        nodes = len(self.trips[0]["path"])
        # Go as far from node to node as possible with only full trips
        while current < nodes:
            #dist = abs(distance_to_meters(self.trips[0]["path"][current-1], self.trips[0]["path"][current]))
            dist = G[self.trips[0]["path"][current-1]][self.trips[0]["path"][current]]["distance"] * 0.3048
            if can_move > dist:
                can_move -= dist
            else:
                break
            current += 1
        if current == nodes:
            self.position = self.trips[0]["path"][-1]
            self.complete_trip()
            return
        # Remove nodes we just traveled
        self.position = self.trips[0]["path"][current-1]
        for i in range(current-2):
            self.trips[0]["path"].pop(0)
        # Travel part of of edge but not full
        to = self.trips[0]["path"][1]
        x1, y1 = distance_to_meters((40.74345679662331, -73.72770035929027), (self.position[0], -73.72770035929027)), distance_to_meters((40.74345679662331, -73.72770035929027), (40.74345679662331, self.position[1]))
        x2, y2 = distance_to_meters((40.74345679662331, -73.72770035929027), (to[0], -73.72770035929027)), distance_to_meters((40.74345679662331, -73.72770035929027), (40.74345679662331, to[1]))
        x_dif = x2 - x1
        y_dif = y2 - y1
        if y_dif == 0:
            if x_dif > 0:
                self.angle = math.pi / 2
            if x_dif < 0:
                self.angle = -1 * math.pi / 2
        else:
            self.angle = abs(math.atan(x_dif / y_dif))
            if y_dif < 0:
                if x_dif > 0:
                    self.angle += math.pi / 2
                else:
                    self.angle += math.pi
            else:
                if x_dif < 0:
                    self.angle -= math.pi / 2
        x_move = can_move * math.sin(self.angle)
        y_move = can_move * math.cos(self.angle)
        #print(self.angle, x_dif, y_dif, x_move, y_move)
        if abs(x_dif) <= abs(x_move) or abs(y_dif) <= abs(y_move):
            #print(1)
            self.position = to
        else:
            # x1, y1 = distance_to_meters((40.74345679662331, -73.72770035929027), (self.position[0], -73.72770035929027)), distance_to_meters((40.74345679662331, -73.72770035929027), (40.74345679662331, self.position[1]))
            # plt.plot([y1 + y_move], [x1 + x_move], "bo")
            lat_per_1d = 111000
            lon_per_1d = math.cos(self.position[0]) * 111321
            #print(to[0] - self.position[0], to[1] - self.position[1], x_move / lat_per_1d, y_move / lon_per_1d)
            if to[0] - self.position[0] <= x_move / lat_per_1d or to[1] - self.position[1] <= y_move / lon_per_1d:
                self.position = to
            else:
                self.position = self.position[0] + x_move / lat_per_1d, self.position[1] + y_move / lon_per_1d
        if self.position == to:
            self.trips[0]["path"].pop(0)
            if len(self.trips[0]["path"]) == 1:
                self.complete_trip()
        else:
            self.trips[0]["path"][0] = self.position


        # can_move = self.current_speed
        # current = 1
        # nodes = len(self.trips[0]["path"])
        # # Go as far from node to node as possible with only full trips
        # while 0 < abs(can_move) and current < nodes:
        #     dist = abs(distance_to_meters(self.trips[0]["path"][current-1], self.trips[0]["path"][current]))
        #     if can_move > dist:
        #         can_move -= dist
        #     else:
        #         break
        #     current += 1
        # if current == nodes:
        #     self.position = self.trips[0]["path"][-1]
        #     self.complete_trip()
        #     return
        # # Remove nodes we just traveled
        # self.position = self.trips[0]["path"][current-1]
        # for i in range(current-2):
        #     self.trips[0]["path"].pop(0)
        # # Travel part of of edge but not full
        # to = self.trips[0]["path"][1]
        # lat_per_1d = 111000
        # lon_per_1d = math.cos(self.position[0]) * 111321
        # lat_dif = to[0] - self.position[0]
        # lon_dif = to[1] - self.position[1]
        # if lon_dif == 0:
        #     if lat_dif > 0:
        #         self.angle += math.pi / 2
        #     if lat_dif < 0:
        #         self.angle += -1 * math.pi / 2
        # else:
        #     self.angle = abs(math.atan((lat_dif * lat_per_1d) / (lon_dif * lon_per_1d)))
        # if lon_dif < 0:
        #     if lat_dif > 0:
        #         self.angle += math.pi / 2
        #     else:
        #         self.angle += math.pi
        # else:
        #     if lat_dif < 0:
        #         self.angle -= math.pi / 2

        # if 0 < self.angle < math.pi / 2: 
        #     print(self.angle, lat_dif, lon_dif)
        # print(self.angle)
        # lat_move = can_move * math.sin(self.angle) / lat_per_1d
        # lon_move = can_move * math.cos(self.angle) / lon_per_1d
        # if abs(lat_dif) <= abs(lat_move) or abs(lon_dif) <= abs(lon_move):
        #     #print(1, lat_move - lat_dif, lon_move-lon_dif)
        #     print(1)
        #     lat_move = lat_dif
        #     lon_move = lon_dif
        # self.position = self.position[0] + lat_move, self.position[1] + lon_move
        # if self.position == to:
        #     self.trips[0]["path"].pop(0)
        #     if len(self.trips[0]["path"]) == 1:
        #         self.complete_trip()
        # else:
        #     self.trips[0]["path"][0] = self.position


        # to = self.trips[0]["path"][1]
        # lat_dif = to[0] - self.position[0]
        # lon_dif = to[1] - self.position[1]
        # if lat_dif == 0:
        #     self.angle = math.atan(lon_dif / 1)
        # else:
        #     self.angle = math.atan(lon_dif / lat_dif)
        # lat_move = self.current_speed * math.cos(self.angle)
        # lon_move = self.current_speed * math.sin(self.angle)
        # print(lat_move, lon_move, lat_dif, lon_dif)
        # if lat_dif < lat_move or lon_dif < lon_move:
        #     lat_move = lat_dif
        #     lon_move = lon_dif
        # self.position = self.position[0] + lat_move, self.position[1] + lon_move
        # if self.position == to:
        #     self.trips[0]["path"].pop(0)
        #     if len(self.trips[0]["path"]) == 1:
        #         self.complete_trip()


# === Main ===
if __name__ == "__main__":
    v1 = Vehicle((40.74345679662331, -73.72770035929027), 200.0, 10.0, 20.0, True, 4)
    from astar import load_data
    G, trips = load_data(reset=False, graph=False, trips=False, abbr=False)
    plt.ion()
    #plt.axis('equal')
    draw_graph(G, bounds=((40.74345679662331, -73.72770035929027), (40.77214782804362, -73.76426798716528)))

    # n1 = (40.74345679662331, -73.72770035929027)
    # n2 = (40.77214782804362, -73.76426798716528)
    # for edge in G.edges():
    #     if min(n1[0],n2[0]) < edge[0][0] < max(n1[0],n2[0]) and min(n1[1],n2[1]) < edge[0][1] < max(n1[1],n2[1]):
    #         x1, y1 = distance_to_meters((40.74345679662331, -73.72770035929027), (edge[0][0], -73.72770035929027)), distance_to_meters((40.74345679662331, -73.72770035929027), (40.74345679662331, edge[0][1]))
    #         x2, y2 = distance_to_meters((40.74345679662331, -73.72770035929027), (edge[1][0], -73.72770035929027)), distance_to_meters((40.74345679662331, -73.72770035929027), (40.74345679662331, edge[1][1]))
    #         plt.plot((y1, y2), (x1, x2), 'c.-')
    v1.assign_trip(G, (40.74345679662331, -73.72770035929027), (40.77214782804362, -73.76426798716528), diste)
    total = 0
    while not v1.available:
        v1.move(G)
        #print(v1.position)
        # x1, y1 = distance_to_meters((40.74345679662331, -73.72770035929027), (v1.position[0], -73.72770035929027)), distance_to_meters((40.74345679662331, -73.72770035929027), (40.74345679662331, v1.position[1]))
        # plt.plot([y1], [x1], "mo")
        plt.plot([v1.position[1]], [v1.position[0]], "mo")
        plt.draw()
        total+=1
        print(total)
        plt.pause(0.00001)
    plt.show()
    # New Variables - Trip
    # Takes care of the trips
    # Scheduling and Admission control - make file/class
    # Server controls and uses the classes
    # Look back at paper

    # Look into fuel efficiency
    # How will simualtion work
