
class Restaurant(object):
    def __init__(self,table_array):
        self.table_dict = self.init_tables(table_array)
        self.total_capacity = self.calc_total_capacity(table_array)
      
      #table information is stored as an array of tuples
      #ie: [(6,1),(2,1),(4,2)] represents 1 table with
      #capacity 6, 1 table with capacity 2 and 1 table
      #with capacity 4
      #the purpose of this function is to create a dictionary of
      #table objects where each key of the dictionary is the capacity of the table
      #ie: [(6,1),(2,1),(4,1)] turns into the dictionary
      #{6:[table_object],2:[table_object],4:[table_object,table_object]}


      # we might just want to make a constructor where we pass in Tables
      # rather than table_tuples
      # (something to think about)
    def init_tables(self,table_array):
        table_dict = []
        for table_tuple in table_array:
            arr = []
            capacity = table_tuple[0]
            num_tables = table_tuple[1]
            meal_duration = 4
            max_duration = 20
            #create a table object for each table of our given capacity
            #and append it to our array
            for i in range(num_tables):
              new_table = Table(capacity,meal_duration,max_duration)
              table_dict.append(new_table)
        return table_dict
      
    def calc_total_capacity(self,table_array):
        total = 0
        for table_tuple in table_array:
            capacity = table_tuple[0]
            num_tables = table_tuple[1]
            total += capacity * num_tables
        return total
    
class Table(object):
    #A table is occupied once there are people at the
    #table. No more people can be seated at the same
    #table even if there are seats available
    def __init__(self,capacity,meal_duration,max_duration):
        self.capacity = capacity
        self.meal_duration = meal_duration
        #invariant for the array below is that the tuples
        #are sorted in ascending order where the first tuple is
        #always (0,x) where x is some end time
        self.available = [(0, max_duration)]
        self.max_duration = max_duration
    
    
    #count must be at least 1
    def turn_count(self):
        count = 0
        for (start,end) in self.available:
            count += (end-start)/self.meal_duration
        return count
    
    # calculate's probability of accepting alternate time slot
    # based on how far the suggested start time is from
    # the original start time
    def accept_probability(self,start_time,discount):
        optimal_suggestion = self.available[0][1]
        #below is safe since we have already called seat on this start time
        #can extend this part to search for all possible time slots
        if discount == None:
            return round(1 - ((start_time-optimal_suggestion)/self.max_duration),2)
        else:
            original_prob = round(1 - ((start_time-optimal_suggestion)/self.max_duration),2)
            discount_incentive = round(((start_time-optimal_suggestion)/self.max_duration),2) * discount
            return original_prob + discount_incentive
    
    def optimal_time(self):
        return self.available[0][1]

    def seat(self,start_time):
        for index in range(len(self.available)):
            (start,end) = self.available[index]
            if start <= start_time and start_time + self.meal_duration < end:
                self.available.pop(index)
                self.available.insert(index, (start, start_time))
                #below should be index + 1 not index please confirm this
                self.available.insert(index+1, (start_time+self.meal_duration, end))
                return True
        return False

    def unseat(self,start_time): # assume this is called on a valid reservation
        for index in range(len(self.available)):
            (start,end) = self.available[index]
            if start_time > start and start_time <= end: # in the right spot
                if start_time == end:
                    self.available[index] = (start, end+self.meal_duration)
        # coalesce
        to_pop = []
        for index in range(1, len(self.available)):
            (start1,end1) = self.available[index-1]
            (start2,end2) = self.available[index]
            if end1 == start2:
                self.available[index-1] = (start1,end2)
                to_pop.append(index)
        for index in to_pop:
            self.available.pop(index)
                
            
            