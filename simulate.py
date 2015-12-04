import math
import random
from objects import *

#generate customers according to a poisson process
def nextCustomers(rate):
    return -math.log(1.0 - random.random()) / rate


def run_simulation():
    #testing to see if oop implementation is working properly
    table_array = [(6,1),(2,1),(4,2)]
    union_grill = Restaurant(table_array)
    
    naive=[]
    heuristic1=[]
    heuristic2=[]
    heuristic3=[]
    for x in xrange(0,200):
        naive.append(run_naive(union_grill,))
        heuristic1.append(run_extends(union_grill,)
        heuristic2.append(run_extends(union_grill,)
        heuristic3.append(run_extends(union_grill,)
    print 1.0*sum(naive)/len(naive)
    print 1.0*sum(heuristic1)/len(heuristic1)
    print 1.0*sum(heuristic2)/len(heuristic2)
    print 1.0*sum(heuristic3)/len(heuristic3)
    #test
    print union_grill.total_capacity 
    print union_grill.table_dict
    
    
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