
class restaurant(object):
      def __init__(self,table_array):
          self.tables = self.init_tables(table_array)
          self.total_capacity = self.calc_total_capacity(table_array)
      
      #table information is stored as an array of tuples
      #ie: [(6,1),(2,1),(4,1)] represents 1 table with
      #capacity 6, 1 table with capacity 2 and 1 table
      #with capacity 4
      #the purpose of this function is to create an array of
      #table objects for each different type of table 
      def init_tables(self,table_array):
          arr = []
          for table_tuple in table_array:
              capacity = table_tuple[0]
              num_tables = table_tuple[1]
              #create a table object for each table of our given capacity
              #and append it to our array
              for i in range(num_tables):
                new_table = table(capacity)
                arr.append(new_table)
          return arr
        
      def calc_total_capacity(self,table_array):
          total = 0
          for table_tuple in table_array:
               capacity = table_tuple[0]
               num_tables = table_tuple[1]
               total += capacity * num_tables
          return total
    
class table(object):
    #A table is occupied once there are people at the
    #table. No more people can be seated at the same
    #table even if there are seats available
    def __init__(self,capacity):
        self.capacity = capacity
        self.seated = 0
        self.available_seating = capacity
        self.occupied = False
    
    #seat people at a table
    def seat_people(self,num_customers):
        if self.available_seating > capacity:
            print "cannot seat more people than their are seats"
        else:
            self.seated = new_customers
            self.available_seating = capacity - new_customers
            self.occupied = True
            
            