import sys
from datetime import datetime, timedelta

from scheduling import *
from vehicle import *
from astar import load_data, draw_graph
from random import randint

if len(sys.argv) not in [2,3]:
        sys.exit("Usage: python simulation.py vehicle_number reset\nvehicle_number - int\nreset - True/False")

# Get start up data
try:
    num_of_vehicles = int(sys.argv[1])
except:
    sys.exit("Usage: python simulation.py vehicle_number reset\nvehicle_number - int\nreset - True/False")

# Load graph and trips
G, trips = None, None
if len(sys.argv) == 3 and sys.argv[2] == "True":
    G, trips = load_data(reset=True, graph=False, trip=False, abbr=False)
else:
    G, trips = load_data(reset=False, graph=False, trip=False, abbr=False)
nodes = G.nodes()
num_nodes = len(nodes) - 1
total_trips = len(trips)

# Create objects
scheduling = Scheduling(G)
for v in range(num_of_vehicles):
    scheduling.vehicles.append(Vehicle(list(nodes)[randint(0, num_nodes)], 40.0, 10.0, 20, True, 4, v))

# Create timer (in seconds)
time = datetime(2015, 1, 1, 0, 0)
#"%m/%d/%y %H:%M:%S", "%m/%d/%y", "%H:%M:%S", "%d %b %y" datetime.strptime(s, keys[key])

# Start simulation:
# 2,678,400 seconds per 31 day month
print(total_trips)
t = 0
interval = 1
while time < datetime(2015, 1, 20, 0, 0):
    while t < total_trips:
        if time == trips[t]["pickup_time"]: # time = time trip was assigned IRL
            scheduling.find_assign_trip(trips[t], diste)
            t += 1
            print("Trip", t)
        if time > trips[t]["pickup_time"]:
            t += 1
            print("skip", t)
        else:
            break
    #print(time)
    interval += 1
    if interval == 5:
        scheduling.move(5)
        interval = 0
    time += timedelta(seconds=1)
print(scheduling.get_logs())
print(len(scheduling.log))