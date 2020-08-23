import sys
from datetime import datetime, timedelta

from scheduling import *
from vehicle import *
from astar import load_data, draw_graph, draw_path
from random import randint

if len(sys.argv) not in [3, 4]:
    sys.exit("Usage: python simulation.py vehicle_number trip_number reset\nvehicle_number - int\ntrip_number - int\nreset - True/False")

# Get start up data
try:
    num_of_vehicles = int(sys.argv[1])
    num_of_trips = int(sys.argv[2])
except:
    sys.exit("Usage: python simulation.py vehicle_number trip_number reset\nvehicle_number - int\ntrip_number - int\nreset - True/False")

# Load graph and trips
G, trips = None, None
if len(sys.argv) == 4 and sys.argv[2] == "True":
    G, trips = load_data(reset=True, graph=False, trip=False, abbr=False)
else:
    G, trips = load_data(reset=False, graph=False, trip=False, abbr=False)
trips = trips[:num_of_trips]
trips.sort()
nodes = G.nodes()
num_nodes = len(nodes) - 1
total_trips = len(trips)

# Create Vehicles and other variables
scheduling = Scheduling(G)
for v in range(num_of_vehicles):
    scheduling.vehicles.append(Vehicle(list(nodes)[randint(0, num_nodes)], 40.0, 10.0, 20, True, 4, v))
time = datetime(2015, 1, 1, 0, 0)
s = 0
t = 0

# Start simulation:
sim_start = datetime.now()
print("=== Running Simulation ===")
interval = 1
while time < datetime(2015, 1, 20, 0, 0): # When to stop simulation.
    while t < total_trips:
        if time == trips[t].pickup_time:  # time = time trip was assigned IRL
            if not scheduling.find_assign_trip(trips[t], diste):
                s += 1
            t += 1
        elif time > trips[t].pickup_time:
            t += 1
            s += 1
        else:
            break
    interval += 1
    if interval == 5:
        scheduling.move(5)
        interval = 0
    # scheduling.move(1)
    time += timedelta(seconds=1)
print("Done\n")
sim_end = datetime.now()

# Start interface for user to look through simulation data
used = 0
for v in scheduling.vehicles:
    if v.log != []:
        used += 1

print("=== Simulation Summary ===")
print(f"Runtime: {sim_end - sim_start}")
print(f"{total_trips - s}/{total_trips} trips completed")
print(f"{used}/{num_of_vehicles} vehicles used")

print("\n=== Interactive Simulation Lookup ===")
ipt = input("S to get the summary, V to look through vehicles, T to look through trips, Q to quit: ").lower()
while ipt != "q":
    if ipt == "v":
        ipt = input(f"Enter a vehicle number (0-{len(scheduling.vehicles)-1}): ").lower()
        try:
            ipt = int(ipt)
        except:
            print("Could't convert to int")
            continue
        for v in scheduling.vehicles:
            if v.id == ipt:
                vehicle = v
                print(vehicle)
                if vehicle.log != []:
                    path = []
                    for trip in vehicle.log:
                        path += trip["path"]
                    sa = so = float("inf")
                    ba = bo = -float("inf")
                    for lat, lon in path:
                        sa = min(lat, sa)
                        so = min(lon, so)
                        ba = max(lat, ba)
                        bo = max(lon, bo)
                    draw_graph(G, bounds=((sa, so), (ba, bo)))
                    draw_path(path)
                    plt.show()
                break
    elif ipt == "t":
        ipt = input(f"Enter a trip number (0-{total_trips-1}): ").lower()
        try:
            ipt = int(ipt)
        except:
            print("Could't convert to int")
            continue
        for t in range(total_trips):
            if t == ipt:
                trip = trips[t]
                print(trip)
                break
    elif ipt == "s":
        print("\n=== Simulation Summary ===")
        print(f"Runtime: {sim_end - sim_start}")
        print(f"{total_trips - s}/{total_trips} trips completed")
        print(f"{used}/{num_of_vehicles} vehicles used")
    ipt = input("S to get the summary, V to look through vehicles, T to look through trips, Q to quit: ").lower()
