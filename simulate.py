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