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
    
    
    
    
    

if __name__ == '__main__':
    run_simulation()