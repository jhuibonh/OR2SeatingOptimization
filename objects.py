
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
        table_dict = {}
        for table_tuple in table_array:
            arr = []
            capacity = table_tuple[0]
            num_tables = table_tuple[1]
            #create a table object for each table of our given capacity
            #and append it to our array
            for i in range(num_tables):
              new_table = Table(capacity)
              arr.append(new_table)
            #keys are integers
            table_dict[capacity] = arr
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
    def __init__(self,capacity,meal_duration,total_time):
        self.capacity = capacity
        self.meal_duration = meal_duration
        self.total_time = total_time
        self.available = [(0, max_duration)]

    def turn_count(self):
        count = 0
        for (start,end) in self.available:
            count += (end-start)/meal_duration
        return count

    def seat(self,start_time):
        for index in range(len(self.available)):
            (start,end) = self.available[index]
            if start <= start_time and start_time + self.meal_duration < end:
                self.available.pop(index)
                self.available.insert(index, (start_time+self.meal_duration, end))
                self.available.insert(index, (start, start_time))
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
                



    # below this is deprecated since we're not doing walkins any more
    
    # #seat people at a table
    # def seat_people(self,num_customers):
    #     if self.available_seating > capacity:
    #         print "cannot seat more people than there are seats"
    #     else:
    #         self.seated = num_customers
    #         self.available_seating = capacity - num_customers
    #         self.occupied = True

    # def unseat_people(self):
    #     if self.occupied:
    #         self.occupied = False
    #     else:
    #         print "nobody at table to kick out"
            
            