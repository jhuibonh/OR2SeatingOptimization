
############################################################
# simulate.py                                              #
# Contains a wrapper to test the algorithm on a            #
# small restaurant, designated Union Grill internally      #
# (does not reflect actual Union Grill seating alignment)  #
############################################################

import math
import random
from objects import *
from heuristic import *

#generate customers according to a poisson process
def nextCustomers(rate):
    return -math.log(1.0 - random.random()) / rate


def run_simulation():
    #testing to see if oop implementation is working properly
    val1 = 0
    val2 = 0
    val3 = 0
    simNum = 20
    #run the simulation with the parameters below 20 times
    for i in range(1,simNum):
        table_array = [(6,3),(2,3),(4,3)]
        union_grill = Restaurant(table_array)
        
        naive=[]
        heuristic1=[]
        heuristic2=[]
        heuristic3=[]
        num_requests = 10
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
                                            [],[],pending_size,pending_time,0,3,discount=.125))
            print x
        val1 +=  1.0*sum([c for (a,b,c) in naive])/len(naive)
        val2 += 1.0*sum([c for (a,b,c) in heuristic2])/len(heuristic2)
        val3 +=  1.0*sum([c for (a,b,c) in heuristic3])/len(heuristic3)
        
    print "naive:", val1/20
    print "extended:", val2/20
    print "discounted:", val3/20
    #test

if __name__ == '__main__':
    run_simulation()