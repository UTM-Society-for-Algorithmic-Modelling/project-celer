from shapely.geometry import shape
import fiona
import math
import networkx as nx
import matplotlib.pyplot as plt
geoms =[shape(feature['geometry']) for feature in fiona.open("NYC/geo_export_bc936d52-8027-4235-a886-37100f11cd10.shp")]

# c = 0
# for feature in fiona.open("NYC/geo_export_bc936d52-8027-4235-a886-37100f11cd10.shp"):
#     c += 1
#     if c == 10 or c == 10000:
#         print(shape(feature['geometry']))
#     if c > 10000:
#         break
try:
     from itertools import izip as zip
except ImportError: # will be 3.x series
     pass
# create a Graph
G = nx.Graph()
for line in geoms:
    for seg_start, seg_end in zip(list(line.coords),list(line.coords)[1:]):
        G.add_edge(seg_start, seg_end)
print(len(G.nodes()))
print(len(G.edges()))

# A star
def dist(p1, p2):
    return (pow(abs(p1[0]-p2[0]), 2) + pow(abs(p1[1]-p2[1]), 2))
path = nx.astar_path(G, (-73.87860420004561, 40.86182675618532), (-74.01723549483906, 40.704096847984154), )
px = []
py = []
for p in range(len(path)-1):
    plt.arrow(path[p][0], path[p][1], path[p+1][0]-path[p][0], path[p+1][1]-path[p][1])
    px.append(path[p][0])
    py.append(path[p][1])

# Matplotlib
x = []
y = []
for node in G.nodes():
    x.append(node[0])
    y.append(node[1])
for edge in G.edges():
    plt.plot(edge[0], edge[1], 'rs-', linewidth=1)
    #plt.plot(edge[0][0], edge[0][1], edge[1][0], edge[1][1], marker = 'o')
#plt.plot(x,y, 'g.')
plt.plot(px,py, 'b.')
plt.axis('equal')
plt.show()

# OLD
#nx.draw(G) 
#print("drew")
#plt.savefig("filename.png") 



# options = {
#     'node_color': 'blue',
#     'node_size': 100,
#     'width': 3,
#     'arrowstyle': '-|>',
#     'arrowsize': 12,
# }
# nx.draw_networkx(G, arrows=True, **options)

# import networkx as nx
# import matplotlib.pyplot as plt

# G=nx.read_shp('NYC') 

# plt.subplot(121)
# nx.draw(G, with_labels=True, font_weight='bold')
# plt.subplot(122)
# nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')