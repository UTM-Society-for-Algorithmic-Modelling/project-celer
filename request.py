
class Request():
	"""
	Represents a trip request by the user/system.
	
	===Attributes===
	start: (lat, long)
	stop: (lat, long)
	max_time: int
	seats: int
	selected: bool
	"""
	
	def __init__(self, start, stop, max_time, seats):
		self.start = start
		self.stop = end
		self.max_time = max_time
		self.seats = seats
		self.selected = False
		self.rush = False
		self.night = False

	def is_selected(self):
		return self.selected

	def get_seats(self):
		return self.seats

	def get_time(self):
		return self.max_time

	def stop(self):
		return self.get_stop

	def start(self):
		return self.start

	def select(self):
		self.selected = True

	def rush(self):
		self.rush = True

	def night(self):
		self.night = True

	def is_rush(self):
		return self.rush

	def is_night(self):
		return self.night
