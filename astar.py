from shapely.geometry import shape
import fiona
import math
import random
import networkx as nx
import matplotlib.pyplot as plt


try:
     from itertools import izip as zip
except ImportError: # will be 3.x series
     pass
# Create a Graph
G = nx.Graph()
speeds = {}
# Replace with street abbr
rep = {}
with open("abbr.txt") as rFile:
    for line in rFile:
        line = line.rstrip("\n")
        rep[line.split(" ")[0].upper()] = line.split(" ")[1].upper()
ti = 0
to = 0
for feature in fiona.open("NYC/VZV_Speed Limits/geo_export_6459c10e-7bfb-4e64-ae29-f0747dc3824c.shp"):
    street = feature["properties"]["street"]
    speeds[street] = feature["properties"]["postvz_sl"]
    for i in rep:
        street = street.replace(i, rep[i])
    speeds[street] = feature["properties"]["postvz_sl"]
for feature in fiona.open("NYC/Map/geo_export_24fdfadb-893d-40a0-a751-a76cdefc9bc6.shp"):
    for seg_start, seg_end in zip(list(shape(feature["geometry"]).coords),list(shape(feature["geometry"]).coords)[1:]):
        street = feature["properties"]["st_label"]
        if street in speeds:
            ti += 1
        else:
            to += 1
        divider = speeds.get(street, 0)
        if divider == 0:
            divider = 25
        G.add_edge(seg_start, seg_end, weight = ((seg_start[0]-seg_end[0]) ** 2 + (seg_start[1]-seg_end[1]) ** 2) ** 0.5 / divider)
print(f"Street names recognized: {ti}. Unrecognized: {to}")

# Plot nodes
# x = []
# y = []
# for node in G.nodes():
#     x.append(node[0])
#     y.append(node[1])
#plt.plot(x,y, 'g.')


# Nodes for pathfinding
# n1 = random.randint(0,361678)
# n2 = random.randint(0,361678)
# c = 0
# for node in G.nodes():
#     if c == n1:
#         n1 = node
#     if c == n2:
#         n2 = node
#     c += 1

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
        if t == 1000:
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

# Plot Edges
c = 0
for edge in G.edges():
    #if c % 3 == 0:
    #if min(n1[0],n2[0]) < edge[0][0] < max(n1[0],n2[0]) and min(n1[1],n2[1]) < edge[0][1] < max(n1[1],n2[1]):
    plt.plot((edge[0][0],edge[1][0]), (edge[0][1], edge[1][1]), 'c.-')
    c += 1


# A star
def diste(p1, p2):
    return (pow(abs(p1[0]-p2[0]), 2) + pow(abs(p1[1]-p2[1]), 2))
def distm(p1, p2):
    return abs(p1[0]-p2[0])+ abs(p1[1]-p2[1])
for trip in trips:
    n1 = trip[0]
    n2 = trip[1]
    print(f"Going from {n1} to {n2}")
    # Find path
    path = nx.astar_path(G, n1, n2, distm)
    # Print cost of path
    print(f"Cost of trip: {nx.astar_path_length(G, n1, n2, distm)}")
    # Print number of nodes in path
    print(f"Nodes in trip: {len(path)}")
    # Add path to figure
    px = []
    py = []
    for p in range(len(path)-1):
        plt.plot((path[p][0], path[p+1][0]), (path[p][1], path[p+1][1]), "m--")
        px.append(path[p][0])
        py.append(path[p][1])
    plt.plot(px,py, 'b.')


plt.axis('equal')
plt.show()