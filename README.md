## OR2SeatingOptimization

Purpose: Optimize seating for restaurants 

Contributors: Ajay Phatak, Steven Silverman, J.M. Huibonhoa, Amy Hung


#High-Level walkthrough of naive algorithm:

1. For each request, if the expected table utilization for the case where the current reservation is rejected cannot make up for the immediate value gained from accepting a reservation then we accept the reservation. Otherwise, we reject the reservation
2. We calculate the average expected table utilization by generating random streams of reservations and applying this dynamic programming algorithm to each of these streams. 
3. This algorithm was proposed by John M. Bossert credited below

#High-Level walkthrough of extended algorithm:

1. For each request, if the expected table utilization for the case where the current reservation is rejected cannot make up for the immediate value gained from accepting a reservation then we offer the customer the option to change their reservation to the nearest available timeslot. 
	- This timeslot has some probability p of being accepted and 1-p of being rejected and generates an    
	  immediate value of s' (This extended algorithm was propsed by Jake Feldman credited below)
	- We extend this algorithm further by adding the option of providing a discount if the alternative timeslot 	  is rejected and this same timeslot now has some probability p' > p of being accepted and 1-p' < 1-p of                 being rejected and generates an immediate value of m' < s'
	- We then take the maximum of these two options, and then take the maximum of its result and the value we            get by rejecting this request


Reference and Credit:
John M. Bossert: http://www.google.com/patents/US20090292566, 
Jake Feldman: https://www.math.hmc.edu/seniorthesis/archives/2010/jfeldman/jfeldman-2010-thesis.pdf
