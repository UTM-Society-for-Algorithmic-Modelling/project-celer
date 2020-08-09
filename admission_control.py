from collections import deque
import request
import astar
import scheduling
import fare
#Determine set of requests suitable for scheduling. 

def admission_control(requests, vehicles):
    """
    Given a set of admissible or inadmissible requests. Use a GA to maximize profit and return only admissible requests.
    Returns a dictionary of optimal, admissible request-trip pairs.

    ==Parameters==
    requests: list of requests
    vehicles: list of vehicle fleet  
    """
    #set up requests stacks for faster access, and graph
    maximum = 3000 #DEFINE 
    requests_stack = deque()
    current_request = None #R of i
    requests_r = requests[::-1]
    final_trips = {}
    G, t = load_data(reset=False, graph=False, trip=False, abbr=False)
    
    for i in range(0, len(requests_r)):
        requests_stack.append(requests_r[i])
        print(requests_r[i])

    #build a distance based Tabu list to eliminate inadmissible vehicles
    while(requests_stack):
        tabu_vehicles = []
        current_request = requests_stack.pop()
        for i in range(0, len(vehicles)):
            v = vehicles[i]
            loc = current_request.start 
            if v.available and distance_to_meters(v.position, loc) < maximum:
                tabu_vehicles.append(v)

        solution = genetic_algorithm(current_request, tabu_vehicles)
        final_trips[solution[1]]=solution[0] #does not store invalid trips!!
    del final_trips[-1]
    for key in final_trips:
        key.selected=True
    
    return final_trips

def genetic_algorithm(request, tabu):
    """
    Optimization. Generates the best trip that maximizes profit based on fuel efficiency, distance, time and traffic. 
    Returns a [request, vehicle ID]
    If no vehicles can complete an admissible trip for this request, vehicle ID = -1 
    
    ==Parameters==
    request: a request obj
    tabu: a list of valid potential vehicles 
    """
    current_fitness = -1
    vehicle_id = -1
    for i in range(0, len(tabu)):
        try:
            path = nx.astar_path(G, tabu[i].position, request.end, astar.diste)
            dist = get_distance(path, tabu[i].start, request.end, G)
            estimated_fare = fare.calculate_fare_NYC(dist, False, False)
            profit = fare.profit(estimated_fare, dist)
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
    for p in range(len(path)-1):
        if G[path[p]][path[p+1]]["distance"] not in distances:
            distances.append(G[path[p]][path[p+1]]["distance"])

    return round(sum(distances) * 0.3048, 2)

#if __name__ == "__main__":
    #Sample Test
    #test_requests = []
    #test_vehicles = []
    #d = admission_control(test_requests, test_vehicles)
    #print(test_requests) 
    #print(test_vehicles)
    #print(d)
