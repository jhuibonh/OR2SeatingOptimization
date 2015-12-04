import math
import random
from objects import *
import copy

#global parameters
value_per_seat = 10
total_period = 20 

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
def heuristic_2(restaurant, demandStream):
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
def heuristic_3(restaurant, demandStream):
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
def run_naive (restaurant,num_requests_accepted,accepted,accepted_arrival,pending_request_size,pending_requested_arrival,booked):
    #expected utilization on reject
    reject_utilization = heuristic_1(restaurant,pending_requested_arrival)
    #this is necessary to test whether a reservation makes sense without committing to the reservation
    test_restaurant = copy.deepcopy(restaurant)
    #base case if number of requests accepted is 0 we return the number of seats booked * value_per_seat along with the accepted requests and arrival times
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
        accept_utilization = heuristic_1(test_restaurant,pending_requested_arrival)
        #update parameters to be passed into recursive call
        num_requests_accepted -= 1
        pending_requested_arrival.pop(0)
        pending_request_size.pop(0)
        if reject_utilization > accept_utilization:
            run_naive(restaurant,num_requests_accepted,accepted,accepted_arrival,pending_request_size,pending_requested_arrival,booked)
        else:
            accepted.append(size)
            accepted_arrival.append(time)
            run_naive(test_restaurant,num_requests_accepted,accepted,accepted_arrival,pending_request_size,pending_requested_arrival,booked+size)


#requires: num_requests_accpeted <= total_period same for all other arguments except booked. heruisitc_num <= 3, discount is None if heuristic_num == 2 and a value between 0 and 1 if heuristic_num == 3
def run_extendeds (restaurant,num_requests_accepted,accepted,accepted_arrival,pending_request_size,pending_requested_arrival,revenue,heuristic_num,discount):
    switch = {
        2: heuristic_2,
        3: heuristic_3
    }
    discounted = False
    heuristic_func = switch.get(heuristic_num, lambda: "invalid heurstic function")
    #expected utilization on reject
    reject_utilization = heuristic_func(restaurant,pending_requested_arrival)
    #this is necessary to test whether a reservation makes sense without committing to the reservation
    test_restaurant = copy.deepcopy(restaurant)
    #base case if number of requests accepted is 0 we return the number of seats booked * value_per_seat along with the accepted requests and arrival times
    if num_requests_accepted == 0:
        return (accepted,accepted_arrival,revenue)
    else:
        time = pending_requested_arrival[0]
        size= pending_request_size[0]
        #try accepting the reservation and test it against case where we reject
        for table in test_restaurant.table_dict:
            if table.capacity == size:
                seatable = table.seat(time)
                if not seatable:
                    accept_probability = round(random.uniform(0.1, 1.0), 2)
                    accept_probability_threshold = table.accept_probability(time,discount)
                    if accept_probability > accept_probability_threshold:
                        table.unseat(time)
                    elif heuristic_num == 3: discounted = True     
                 
        accept_utilization = heuristic_func(test_restaurant,pending_requested_arrival)
        #update parameters to be passed into recursive call
        num_requests_accepted -= 1
        pending_requested_arrival.pop(0)
        pending_request_size.pop(0)
        if reject_utilization > accept_utilization:
            run_extendeds(restaurant,num_requests_accepted,accepted,accepted_arrival,pending_request_size,pending_requested_arrival,revenue,heuristic_num)
        else:
            accepted.append(size)
            accepted_arrival.append(time)
            if discounted:
                revenue = revenue + size * value_per_seat * discount
            else:
                revenue = revenue + size * value_per_seat
            run_extendeds(test_restaurant,num_requests_accepted,accepted,accepted_arrival,pending_request_size,pending_requested_arrival,revenue,heuristic_num)  
          

         
