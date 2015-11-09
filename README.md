## OR2SeatingOptimization

Purpose: Optimize seating for restaurants 

Contributors: Ajay Phatak, Steven Silverman, J.M. Huibonhoa, Amy Hung


#High-Level walkthrough of naive algorithm:

1. For each request, if the expected table utilization for the case where the current reservation is rejected cannot make up for the immediate value gained from accepting a reservation then we accept the reservation. Otherwise, we reject the reservation
2. We calculate the average expected table utilization by generating random streams of reservations and applying this dynamic programming algorithm to each of these streams. 

#High-Level walkthrough of extended algorithm:

1. For each request, if the expected table utilization for the case where the current reservation is rejected cannot make up for the immediate value gained from accepting a reservation then we offer the customer the option to change their reservation to the nearest available timeslot. 
	- This timeslot has some probability p of being accepted and 1-p of being rejected and generates an immediate           value of s'
	- We extend this algorithm further by adding the option of providing a discount if the alternative timeslot 		  is rejected and this same timeslot now has some probability p' of being accepted and 1-p' of being                rejected and generates an immediate value of m'
	- We then take the maximum of these two options, and then take the maximum of its result and the value we get           by rejecting this request
