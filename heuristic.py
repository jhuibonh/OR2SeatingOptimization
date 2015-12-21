
###################################################
# Heuristic.py                                    #
# Contains functions to compute the two-pass      #
# heuristic, as well as run the naive algorithm   #
# and both versions of the extended algorithms    #
###################################################


import math
import random
from objects import *
import copy

#global parameters
value_per_seat = 10
total_period = 20
meal_duration = 4

def randomStream(length):
    arrivals = []
    for i in range(length):
        arrivals.append((random.randint(2,6),random.randint(0, total_period - meal_duration)))
    return arrivals     

# two-pass heuristic to estimate seats-to-go

# below is the heuristic for the naive algorithm
def heuristic_1(restaurant, demandStream):
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
                    fulfilled.append((size,time))
                    #missing append to fulfilled
                    booked += size
                    break # go to next reservation
    return booked

# below is the heuristic for the second extended algorithm in the paper
def heuristic_2(restaurant, demandStream, discount):
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
                    accept_probability = round(random.uniform(0.1, 1.0), 2)
                    accept_probability_threshold = table.accept_probability(time,None)
                    final_count = table.turn_count()
                    if (final_count < initial_count - 1) and (accept_probability > accept_probability_threshold):
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
                    accept_probability = round(random.uniform(0.1, 1.0), 2)
                    accept_probability_threshold = table.accept_probability(time,discount)
                    if (accept_probability > accept_probability_threshold):
                        table.unseat(time)
                    else:
                        fulfilled.append((size,time))
                        booked += size
                        break # got it, so look at next reservation
    return booked * value_per_seat

# below is the heuristic for the our extended algorithm
def heuristic_3(restaurant, demandStream, discount):
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
                    accept_probability = round(random.uniform(0.1, 1.0), 2)
                    accept_probability_threshold = table.accept_probability(time,discount)
                    final_count = table.turn_count()
                    if (final_count < initial_count - 1) and (accept_probability > accept_probability_threshold):
                        table.unseat(time)
                    else:
                        fulfilled.append((size,time))
                        booked += size
                        break # got it, so look at next reservation
    # remove reservations we already made
    demandStream[:] = [x for x in demandStream if not (x in fulfilled)]
    for (size, time) in demandStream:
        for table in restaurant.table_dict:
            if table.capacity >= size:
                seatable = table.seat(time)
                if seatable:
                    accept_probability = round(random.uniform(0.1, 1.0), 2)
                    accept_probability_threshold = table.accept_probability(time,discount)
                    if (accept_probability > accept_probability_threshold):
                        table.unseat(time)
                    else:
                        fulfilled.append((size,time))
                        booked += size
                        break # got it, so look at next reservation
    return booked * value_per_seat

#requires: num_requests_accpeted <= total_period same for all other arguments except booked. heruisitc_num <= 3
def run_naive (restaurant,num_requests_accepted,accepted,accepted_arrival,pending_request_size,
               pending_requested_arrival,booked):
    #expected utilization on reject
    reject_utilization = 0
    sim_streams = 50
    for i in range(len(pending_requested_arrival)):
        reject_utilization += heuristic_1(restaurant,randomStream(sim_streams))
    reject_utilization /= float(sim_streams)
    #this is necessary to test whether a reservation makes sense without committing to the reservation
    test_restaurant = copy.deepcopy(restaurant)
    #base case if number of requests accepted is 0 we return the number of seats booked * value_per_seat
    #along with the accepted requests and arrival times
    if num_requests_accepted == 0:
        return (accepted,accepted_arrival,booked * value_per_seat)
    else:
        time = pending_requested_arrival[0]
        size = pending_request_size[0]
        #try accepting the reservation and test it against case where we reject
        for table in test_restaurant.table_dict:
            if table.capacity == size:
                seatable = table.seat(time)
                if not seatable: table.unseat(time)
        accept_utilization = 0  
        for i in range(len(pending_requested_arrival)):
            accept_utilization += heuristic_1(restaurant,randomStream(sim_streams))
        accept_utilization /= float(sim_streams)
        #update parameters to be passed into recursive call
        num_requests_accepted -= 1
        pending_requested_arrival.pop(0)
        pending_request_size.pop(0)
        if reject_utilization > accept_utilization:
            return run_naive(restaurant,num_requests_accepted,accepted,accepted_arrival,pending_request_size,
                             pending_requested_arrival,booked)
        else:
            accepted.append(size)
            accepted_arrival.append(time)
            return run_naive(test_restaurant,num_requests_accepted,accepted,accepted_arrival,pending_request_size,
                             pending_requested_arrival,booked+size)


#requires: num_requests_accpeted <= total_period same for all other arguments except booked. heruisitc_num <= 3
#discount is None if heuristic_num == 2 and a value between 0 and 1 if heuristic_num == 3
def run_extendeds (restaurant,num_requests_accepted,accepted,accepted_arrival,pending_request_size,
                   pending_requested_arrival,revenue,heuristic_num,discount=None):
    switch = {
        2: heuristic_2,
        3: heuristic_3
    }
    discounted = False
    reject_utilization = 0
    sim_streams = 50
    heuristic_func = switch.get(heuristic_num, lambda: "invalid heuristic function")
    #expected utilization on reject
    for i in range(len(pending_requested_arrival)):
        reject_utilization += heuristic_func(restaurant,randomStream(sim_streams),discount)
    reject_utilization /= float(sim_streams)
    #this is necessary to test whether a reservation makes sense without committing to the reservation
    test_restaurant = copy.deepcopy(restaurant)
    #base case if number of requests accepted is 0 we return the number of seats booked * value_per_seat
    #along with the accepted requests and arrival times
    if len(pending_requested_arrival) == 0:
        return (accepted,accepted_arrival,revenue)
    else:
        time = pending_requested_arrival[0]
        size = pending_request_size[0]
        #try accepting the reservation and test it against case where we reject
        for table in test_restaurant.table_dict:
            if table.capacity == size:
                seatable = table.seat(time)
                if not seatable:
                    #capping accept probability at 70 percent
                    accept_probability = round(random.uniform(0.1, 0.7), 2)
                    accept_probability_threshold = table.accept_probability(time,discount)
                    if accept_probability > accept_probability_threshold:
                        table.unseat(time)
                    elif heuristic_num == 3: discounted = True     
        accept_utilization = 0
        for i in range(len(pending_requested_arrival)):
            accept_utilization += heuristic_func(restaurant,randomStream(sim_streams),discount)
        accept_utilization /= float(sim_streams)
        #update parameters to be passed into recursive call
        num_requests_accepted -= 1
        pending_requested_arrival.pop(0)
        pending_request_size.pop(0)
        if reject_utilization > accept_utilization:
            return run_extendeds(restaurant,num_requests_accepted,accepted,accepted_arrival,pending_request_size,
                                 pending_requested_arrival,revenue,heuristic_num,discount)
        else:
            accepted.append(size)
            accepted_arrival.append(time)
            if discounted:
                revenue = revenue + size * value_per_seat * (1-discount)
            else:
                revenue = revenue + size * value_per_seat
            return run_extendeds(test_restaurant,num_requests_accepted,accepted,accepted_arrival,pending_request_size,
                                 pending_requested_arrival,revenue,heuristic_num,discount)
          

         
