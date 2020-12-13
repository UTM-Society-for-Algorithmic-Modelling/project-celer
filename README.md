# project-celer
# Objective

Celer's objective is to solve the problem of car interconnectivity to minimize traffic and optimize for efficiency. As society moves closer to fully autonomous vehicles, we must eventually make vehicles work together: reduce traffic jams, reduce cost of trips, reduce overall travel time, reduce the environmental impact, and reduce the number of casualties to traffic. 

# Goals

To use pathfinding algorithms to find optimal routes. To maximize traffic efficiency by having vehicles be perfectly synchronized allowing for high speeds, no traffic lights, and minimal stoppage/slow moments. Incorporate a way for pedestrians and bicycles to be included in the traffic while minimizing their impact on overall efficiency. To find a way to store the vehicles currently not in use without having a significant impact on cost and efficiency.

# Solution

Using a combination of machine learning, algorithms, a central database, multiple smaller local databases, and live feedback to enhance traffic. A simulation will be used to simulate traffic in realistic conditions in which vehicles will communicate relevant information to a central database. As new situations arise it will be solved locally if possible, otherwise it will be communicated to the central database where a solution will be found quickly.

# Sources

2015 Yellow Taxi Data - https://data.cityofnewyork.us/Transportation/2015-Yellow-Taxi-Trip-Data/ba8s-jw6u
Speed Map - https://data.cityofnewyork.us/Transportation/VZV_Speed-Limits/7n5j-865y
City Map - https://data.cityofnewyork.us/City-Government/NYC-Street-Centerline-CSCL-/exjm-f27b
Traffic Data (2014-2018) format: ROADWAYNAME 0-24HRS - https://data.cityofnewyork.us/Transportation/Traffic-Volume-Counts-2014-2018-/ertz-hr4r
