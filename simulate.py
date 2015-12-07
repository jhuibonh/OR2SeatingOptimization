import math
import random
from objects import *
from heuristic import *

#generate customers according to a poisson process
def nextCustomers(rate):
    return -math.log(1.0 - random.random()) / rate


def run_simulation():
    #testing to see if oop implementation is working properly
    table_array = [(6,3),(2,3),(4,3)]
    union_grill = Restaurant(table_array)
    
    naive=[]
    heuristic1=[]
    heuristic2=[]
    heuristic3=[]
    num_requests = 20
    for x in xrange(0,10):
        pending = randomStream(num_requests)
        pending_size = [size for (size,time) in pending]
        pending_time = [time for (size,time) in pending]
        naive.append(run_naive(union_grill,num_requests,
                               [],[],pending_size,pending_time,0))
        #heuristic1.append(run_extendeds(union_grill,num_requests,
        #                                [],[],pending_size,pending_time,0))
        pending_size = [size for (size,time) in pending]
        pending_time = [time for (size,time) in pending]
        heuristic2.append(run_extendeds(restaurant=union_grill,num_requests_accepted=num_requests,
                                        accepted=[],accepted_arrival=[],
                                        pending_request_size=pending_size,
                                        pending_requested_arrival=pending_time,revenue=0,heuristic_num=2))
        pending_size = [size for (size,time) in pending]
        pending_time = [time for (size,time) in pending]
        heuristic3.append(run_extendeds(union_grill,num_requests,
                                        [],[],pending_size,pending_time,0,3,discount=.15))
        print x
    print "naive:", 1.0*sum([c for (a,b,c) in naive])/len(naive)
    #print 1.0*sum(heuristic1)/len(heuristic1)
    print "extended:", 1.0*sum([c for (a,b,c) in heuristic2])/len(heuristic2)
    print "discounted:", 1.0*sum([c for (a,b,c) in heuristic3])/len(heuristic3)
    #test

    
    
############################################################
# Plan is to randomly generate customers,                  #
# then try several algorithms and minimizations            #
#                                                          #
# Can minimize avg wait time, max wait time                #
# Can maximize utilization (from restaurant's POV)         #
# Can use greedy, randomized, assignment algo, etc.        #
#                                                          #
# Analyze and pick the best one for various situations     #
############################################################
    
    

if __name__ == '__main__':
    run_simulation()