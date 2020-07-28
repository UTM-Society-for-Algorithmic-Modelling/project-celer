# project-celer
Objective

As society moves closer and closer to fully autonomous vehicles, we will eventually get to the problem of having to make the vehicles work together so as to make everything as efficient as possible: reduce traffic jams, reduce cost of trips, reduce overall travel time, reduce the environmental impact, and reduce the number of casualties to traffic. The objective is to solve the problem of car interconnectivity to minimize traffic and optimize for efficiency in terms of time and cost for things like gas and maintenance.

Goals

To use pathfinding algorithms to find optimal routes. To maximize traffic efficiency by having vehicles be perfectly synchronized allowing for high speeds, no traffic lights, and minimal stoppage/slow moments. To incorporate a way for pedestrians and bicycles to be included in the traffic while minimizing their impact on overall efficiency. To find a way to store the vehicles currently not in use without having a significant impact on cost and efficiency.

Solution

Using a combination of machine learning, algorithms, a central database, multiple smaller local databases, and live feedback to enhance traffic. A simulation will be used to simulate traffic in realistic conditions in which vehicles will communicate realistic information to a central database where machine learning algorithms will be used to instruct the vehicles of their path, required speed, and more information. As new situations happen, like maybe a vehicle gets a new destination or a pedestrian wants to cross, everything will be solved locally if possible, otherwise it will be communicated to the central database where a solution will be found quickly.

Sources
2015 Yellow Taxi Data - https://data.cityofnewyork.us/Transportation/2015-Yellow-Taxi-Trip-Data/ba8s-jw6u
Speed Map - https://data.cityofnewyork.us/Transportation/VZV_Speed-Limits/7n5j-865y
City Map - https://data.cityofnewyork.us/City-Government/NYC-Street-Centerline-CSCL-/exjm-f27b