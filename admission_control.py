from collections import deque
import networkx as nx
import request
import scheduling
import astar
import fare

# Determine set of requests suitable for scheduling.

maximum_radius = 3000


def admission_control(request, vehicles, G):
    """
    Given an admissible or inadmissible request: Use a GA to maximize profit and return an optimal request, vehicle pair
    if admissible.
 
    returns {vehicle ID: request}
    ==Parameters==
    request: Request() object
    vehicles: list of vehicles (total fleet)  
    """
   
    final_trip = {}
    tabu_vehicles = [] #Build a distance based Tabu list for possible vehicles
    #G, t = astar.load_data(reset=False, graph=False, trip=False, abbr=False)

    for i in range(0, len(vehicles)):
        v = vehicles[i]
        loc = request.start
        if v.available and astar.distance_to_meters(v.position, loc) < maximum_radius:
            tabu_vehicles.append(v)

    solution = genetic_algorithm(request, tabu_vehicles, G)
    final_trip[solution[1]] = solution[0]  # will not store invalid trips!!

    for key in final_trip:
        r = final_trip[key]
        r.select()

    return final_trip


def genetic_algorithm(request, tabu, G):
    """
    Modelled after the one found in the research paper. Generates the best trip that maximizes profit based on fuel efficiency, distance, time and traffic. 
    Returns a [request, vehicle].
    If no vehicles can complete an admissible trip for this request, vehicle = -1.
    
    ==Parameters==
    request: a request obj
    tabu: a list of valid potential vehicles
    G: a networkx graph 
    """
    current_fitness = -1
    vehicle_id = -1
    try:
        path = nx.astar_path(G, request.start, request.stop, astar.diste)
        main_distance = get_distance(path, request.start, request.stop, G)
    except:
        return [request, -1]

    for i in range(0, len(tabu)):
        try:
            arrival_path = nx.astar_path(G, tabu[i].position, request.start, astar.diste)
            total_distance = get_distance(arrival_path, tabu[i].position, request.start, G) + main_distance
            estimated_fare = fare.calculate_fare_NYC(total_distance, False, False)
            profit = fare.profit(estimated_fare, total_distance)
            if profit > current_fitness:
                current_fitness = profit
                vehicle_id = tabu[i].id
        except:
            break

    return [request, vehicle_id]


def get_distance(path, n1, n2, G):
    """
    Given a path of nodes, calculates the total road distance.

    ==Parameters==
    path: list of nodes
    n1: (lat, long)
    n2: (lat, long)
    G: road networkx graph
    """
    distances = []
    for p in range(len(path) - 1):
        if G[path[p]][path[p + 1]]["distance"] not in distances:
            distances.append(G[path[p]][path[p + 1]]["distance"])

    return round(sum(distances) * 0.3048, 2)
