from astar import diste, print_trip_info
import networkx as nx


class Vehicle():

    def __init__(self, position, maximum_speed, fuel, current_speed, available, seats):
        self.position = position
        self.maximum_speed = maximum_speed
        self.fuel = fuel
        self.current_speed = current_speed
        self.available = available
        self.seats = seats

    def is_available(self):
        """
        Return self.available.
        """
        return self.available

    def distance_to(self, p, G):
        """
        Return the distance from self.position to p.

        Parameters: (self, p, G)
            p - (lat, lon)
            G - networkx.graph()
        """
        path = nx.astar_path(G, self.position, p, diste)
        return print_trip_info(self.position, p, path, G)[1]


# === Main ===
if __name__ == "__main__":
    v1 = Vehicle((40.74345679662331, -73.72770035929027), 200, 10, 0, True, 4)
    from astar import load_data
    G, trips = load_data(reset=False, graph=False, trips=False, abbr=False)
    v1.distance_to((40.77214782804362, -73.76426798716528), G)