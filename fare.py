import math

#This sets and uses a fare function to calculate the profit made during runs/trips.
#live

def calculate_fare_NYC(distance, rush, overnight):
	"""
	Calculate a standard NYC fare. Return revenue function r(x).
	Source: https://www1.nyc.gov/site/tlc/passengers/taxi-fare.page#:~:text=%242.50%20initial%20charge.,Dutchess%2C%20Orange%20or%20Putnam%20Counties.

	Initial charge: $2.50
	Per metre: $0.00155344
	Rush Hour: +$1.00
	Overnight: +$0.50
	
	f(x)=(0.00155344x+2.50)
	g(x)=(0.00155344x+2.50)+1
	h(x)=(0.00155344x+2.50)+0.50
	
	==Parameters==
	distance: float (Trip distance in metres)
	rush: bool
	overnight: bool
	"""
	if rush:
		return (0.00155344*distance) + (2.50+1)
	elif overnight:
		return (0.00155344*distance) + (2.50+0.50)
	else:
		return (0.00155344*distance) + (2.50)


#def calculate_fare_TO(rush, overnight) Optional 
#	"""
#	b/docs/articles/municipal-licensing-and-standards/bylaw-enforcement/licensing-enforcement/taxis-taxicabs-vehicle-for-hire-accessible-taxis-fares-city-of-toronto.html
#	"""

def profit(fare, distance):
	"""
	Return profit using profit function: p(x)=r(x)-c(x).
	Uses a standard fuel cost estimate.

	==Parameters==
	fare: float
	distance: float (metres)
	"""
	return fare - cost(distance)

def cost(distance):
	"""
	Calculates the cost to run a trip. Returns a c(x) function.

	July 21, 2020: $0.89/L of fuel in NYC 
	Fuel Efficiency (Avg Estimate): 9.4L/100 km  

	c(x) = price * ((distance * price)/fuel efficiency)
	==Parameters==
	distance: distance in metres 
	"""
	d = distance/1000
	price = 0.89
	fuel_e = 9.4

	amount = (d * price)/fuel_e
	return price * amount
	
