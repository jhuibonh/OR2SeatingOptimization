import math
import random
from objects import *

#generate customers according to a poisson process
def nextCustomers(rate):
    return -math.log(1.0 - random.random()) / rate


def run_simulation():
    #testing to see if oop implementation is working properly
    table_array = [(6,1),(2,1),(4,1)]
    union_grill = restaurant(table_array)
    
    
    
    
    
    

if __name__ == '__main__':
    run_simulation()