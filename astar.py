from shapely.geometry import shape
import fiona
import networkx as nx
import matplotlib.pyplot as plt
import math
import random
import pickle
try:
    from itertools import izip as zip
except ImportError:
    pass

def main():
    """
    Main function
    """
    G, trips = load_data(reset=False, graph=False, trips=False, abbr=False)
    t = random_trip(G)
    #t = ((-73.72770035929027, 40.74345679662331), (-73.76426798716528, 40.77214782804362))
    draw_graph(G, bounds=t)
    process_trips(G, trips=[t], heuristic=distm)

    plt.axis('equal')
    plt.show()


# === Load Data ===
def load_data(reset=False, graph=False, trips=False, abbr=False):
    """
    Returns a graph representing the NYC map and an array of 2015 trips.

    Parameters: (reset)
        reset - bool
        graph - bool
        trips - bool
        abbr - bool
    """
    G = None
    trips = None

    if reset:
        graph = trips = True
    if graph:
        pickle_graph(abbr)
    with open('graph.pkl', 'rb') as graph_file:
        G = pickle.load(graph_file)

    if trips:
        pickle_trips(G)
    with open('trips.pkl', 'rb') as trips_file:
        trips = pickle.load(trips_file)

    return G, trips

def pickle_graph(abbr):
    """
    Save the graph in a pickle file.

    Parameters: (abbr)
        abbr - bool
    """
    # Replace with street abbr
    try:
        if abbr:
            raise ResetPickle
        with open('abbr.pkl', 'rb') as abbr_file:
            abbr = pickle.load(abbr_file)
    except:
        abbr = {}
        with open("abbr.txt") as rFile:
            for line in rFile:
                line = line.rstrip("\n")
                abbr[line.split(" ")[0].upper()] = line.split(" ")[1].upper()
        with open('abbr.pkl', 'wb') as out:
            pickle.dump(abbr, out)
        
    recognized = 0
    unrecognized = 0

    # Build speeds dictionary
    speeds = {}
    for feature in fiona.open("NYC/VZV_Speed Limits/geo_export_822d1ee8-4ed3-44b9-a802-eae08ae68732.shp"):
        street = feature["properties"]["street"]
        for v in street_variations(street, abbr):
            speeds[v] = feature["properties"]["postvz_sl"]
    
    # Create a Graph
    G = nx.Graph()
    for feature in fiona.open("NYC/Map/geo_export_0b3bfc39-2b07-4b83-b2d7-50b1be52dd7a.shp"):
        for seg_start, seg_end in zip(list(shape(feature["geometry"]).coords),list(shape(feature["geometry"]).coords)[1:]):
            street = feature["properties"]["st_label"]
            if street in speeds:
                recognized += 1
            else:
                unrecognized += 1
            divider = speeds.get(street, 0)
            if divider == 0:
                divider = 25
            G.add_edge(seg_start, seg_end, weight = weight(seg_start, seg_end, divider), distance=feature["properties"]["shape_leng"])
    
    print(f"Recognized: {recognized}. Unrecognized: {unrecognized}. Percent recognized: {recognized / (unrecognized+recognized) * 100}%.")

    with open('graph.pkl', 'wb') as out:
            pickle.dump(G, out)
    
def pickle_trips(G):
    """
    Saves the trips in a pickle file.

    Parameters: (G)
        G - networkx.graph()
    """
    trips_raw = {}
    with open("NYC/2015_taxi_data.csv") as rFile:
        first_line = rFile.readline().rstrip("\n").split(",")
        t = 0
        for line in rFile:
            line = line.rstrip("\n").split(",")
            temp = {}
            for i in range(len(first_line)):
                temp[first_line[i]] = line[i]
            trips_raw[t] = temp
            t += 1
            if t == 1:
                break
    trips = []
    for trip in trips_raw.values():
        starting = (float(trip["pickup_longitude"]), float(trip["pickup_latitude"]))
        ending = (float(trip["dropoff_longitude"]), float(trip["dropoff_latitude"]))
        n1 = (None, float("inf"))
        n2 = (None, float("inf"))
        for node in G.nodes():
            closeness = abs(starting[0] - node[0]) + abs(starting[1] - node[1])
            if closeness < n1[1]:
                n1 = (node, closeness)
            closeness = abs(ending[0] - node[0]) + abs(ending[1] - node[1])
            if closeness < n2[1]:
                n2 = (node, closeness)
        trips.append((n1[0], n2[0]))
        
    with open('trips.pkl', 'wb') as out:
        pickle.dump(trips, out)

def street_variations(s, abbr):
    """
    Returns multiple variations of the street name based on common street term abbriviations.

    Parameters: (s, abbr)
        s - string
        abbr - {ABBR}
    """
    variations = [s]
    for a in abbr:
        for v in variations.copy():
            if a in v:
                v = v.replace(a, abbr[a])
                variations.append(v)
    return variations

class ResetPickle(Exception):
    pass


# === Plotting ===
def draw_graph(g, bounds=((-180, -90), (180, 90))):
    """
    Plots the edges on matplotlib.

    Parameters: (g, bounds)
        g - networkx.graph()
        bounds - (node, node)
        node - (lon, lat)
    """
    # Plot Edges
    n1 = bounds[0]
    n2 = bounds[1]
    for edge in g.edges():
        if min(n1[0],n2[0]) < edge[0][0] < max(n1[0],n2[0]) and min(n1[1],n2[1]) < edge[0][1] < max(n1[1],n2[1]):
            plt.plot((edge[0][0],edge[1][0]), (edge[0][1], edge[1][1]), 'c.-')

def draw_path(path):
    """
    Plots a path on matplotlib.

    Parameters: (path)
        path - [nodes]
        node - (lon, lat)
    """
    px = []
    py = []
    for p in range(len(path)-1):
        plt.plot((path[p][0], path[p+1][0]), (path[p][1], path[p+1][1]), "m--")
        px.append(path[p][0])
        py.append(path[p][1])
    plt.plot(px,py, 'b.')


# === Trips ===
def process_trips(G, trips, heuristic):
    """
    Processes trips and plots them on the graph

    Parameters: (G, trips, heuristic)
        G - networkx.graph()
        trips - [trips]
        heuristic - Callable
        trip - (node, node)
        node - (lon, lat)
    """
    for trip in trips:
        n1 = trip[0]
        n2 = trip[1]
        print(f"Going from {n1} to {n2}")
        try:
            path = nx.astar_path(G, n1, n2, heuristic)

            print(f"Cost of trip: {nx.astar_path_length(G, n1, n2, heuristic)}")
            print(f"Nodes in trip: {len(path)}")
            # Note: Edges with the exact same length are only counted once as this was found to be the most accurate so far
            speeds = {}
            distances = []
            for p in range(len(path)-1):
                speed = round( 1 / G[path[p]][path[p+1]]["weight"] * ((path[p][0] - path[p+1][0]) ** 2 + (path[p][1] - path[p+1][1]) ** 2) ** 0.5)
                if G[path[p]][path[p+1]]["distance"] not in distances:
                    distances.append(G[path[p]][path[p+1]]["distance"])
                    speeds[speed] = speeds.get(speed, 0) + 1
            print(f"Speeds (mph): {speeds}")
            print(f"Distance (meters?): {round(sum(distances) * 0.3048, 2)}")
            print(f"Euclidean distance (meters): {distance_to_meters(n1, n2)}")

            draw_path(path)
        except:
            print("Couldn't find a path")

def random_trip(G):
    """
    Returns a randomly generated trip.

    Parameters: (G)
        G - netwrokx.graph()
    """
    tn = len(G.nodes())
    n1 = random.randint(0,tn)
    n2 = random.randint(0,tn)
    tn = 0
    for node in G.nodes():
        if n1 == tn:
            n1 = node
        if n2 == tn:
            n2 = node
        tn += 1
    return n1, n2


# === Heuristics ===
def weight(s, e, speed):
    """
    Returns the weight to be assigned to the edges of the graph.

    Parameters: (s, e, d)
        s - (lon, lat)
        e - (lon, lat)
        speed - int
    """
    return ((s[0] - e[0]) ** 2 + (s[1] - e[1]) ** 2) ** 0.5 / speed

def diste(p1, p2):
    """
    Returns euclidean distance divided by the default NYC speed.

    Parameters: (p1, p2)
        p1 - (lon, lat)
        p2 - (lon, lat)
    """
    return (pow(abs(p1[0]-p2[0]), 2) + pow(abs(p1[1]-p2[1]), 2)) ** 0.5 / 65

def distm(p1, p2):
    """
    Returns manhattan distance divided by the default NYC speed.

    Parameters: (p1, p2)
        p1 - (lon, lat)
        p2 - (lon, lat)
    """
    return abs(p1[0]-p2[0])+ abs(p1[1]-p2[1]) / 65


# === Helpers ===
def distance_to_meters(n1, n2):
    """
    Calculates the great circle distance between two points.

    Parameters: (n1, n2)
        n1 - (lon, lat)
        n2 - (lon, lat)
    """
    radius = 6371000 # Radius of earth
    o1 = n1[1] * math.pi / 180
    o2 = n2[1] * math.pi / 180
    d1 = (n2[1] - n1[1]) * math.pi /180
    d2 = (n2[0] - n1[0]) * math.pi /180

    a = math.sin(d1 / 2) * math.sin(d1 / 2) + math.cos(o1) * math.cos(o2) * math.sin(d2/2) * math.sin(d2/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return round(radius * c, 2)


# === Main ===
if __name__ == "__main__":
    main()
