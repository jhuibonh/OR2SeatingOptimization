import math
import random
from objects import *

# two-pass heuristic to estimate seats-to-go

def heuristic(restaurant, currtime, endTime, demandStream):
	mealDuration = 4 # one unit = 15 minutes
	# demandStream is a list of (party size, time)
	# first loop places all exact fit reservations (as described in paper)
	fulfilled = [] # reservations we've booked
	booked = 0 # seats we've booked
	for (size, time) in demandStream:
		for table in restaurant.table_dict:
			if table.capacity == size:
				initial_count = table.turn_count()
				seatable = table.seat(time)
				if seatable:
					final_count = table.turn_count()
					if (final_count < initial_count - 1):
						table.unseat(time)
					else:
						fulfilled.append((size,time))
						booked += size
						break # got it, so look at next reservation
				# otherwise it's booked for that time, so look at other tables
	# remove reservations we already made
	demandStream[:] = [x for x in demandStream if not (x in fulfilled)]
	for (size, time) in demandStream:
		for table in restaurant.table_dict:
			if table.capacity >= size:
				seatable = table.seat(time)
				if seatable:
					booked += size
					break # go to next reservation
	return booked