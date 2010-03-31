import MySQLdb
from sqlalchemy import *
import numpy
import math, time, copy, random, os, sys, subprocess
from data_mining.PrintOutput import PrintOutput

#loads system variables                                                                                  
import os
path = os.environ.get('OPUS_HOME')
path = os.path.join(path, "src", "data_mining", "SYSTEM_VARIABLES.py")
execfile(path) 

class Query_manager :
    def __init__(self, io_info_element, logCB = None, progressCB = None) :
        
        #For reporting results
        self.printOut = PrintOutput(logCB, progressCB, PROFILING)        
        
        #Storing all the information passed as parameters to the query manager
        self.db_url = io_info_element.attributes["input_db_url"].value
        self.table_name = io_info_element.attributes["input_table_name"].value
        self.x_attribute = io_info_element.attributes["x_column"].value
        self.y_attribute = io_info_element.attributes["y_column"].value
        self.id_attribute = io_info_element.attributes["id_column"].value

        #Forcing certain attributes to be categorical
        self.fclass_atts = []
        if io_info_element.hasAttribute('force_to_class') :
            self.fclass_atts = util_get_attribute_list(io_info_element.attributes["force_to_class"].value)

        #Forcing certain attributes to be numerical
        self.fnum_atts = []
        elements = io_info_element.getElementsByTagName('force_to_numeric')
        if io_info_element.hasAttribute('force_to_numeric') :
            self.fnum_atts = util_get_attribute_list(io_info_element.attributes["force_to_numeric"].value)

        #Size of blocks that will be created
        self.train_size = 40000
        if io_info_element.hasAttribute("train_block_size") :
            self.train_size = int(io_info_element.attributes["train_block_size"].value)
        
        self.test_size = 40000
        if io_info_element.hasAttribute("test_block_size") :
            self.test_size = int(io_info_element.attributes["test_block_size"].value)

        #Getting access to the table
        self.table = util_get_table(self.db_url, self.table_name)

        #Getting all attributes from the table
        #Getting what types of attributes they are
        (self.class_list, self.numeric_list, self.attributes) = util_get_attribute_info(self.table, self.fclass_atts, self.fnum_atts)

        #Used for the parcel query
        self.query_string = True
        elements = io_info_element.getElementsByTagName('test_criteria')
        if len(elements) > 0 :
            tc_elem = elements[0]
            self.query_string = self.util_create_query_string(tc_elem)

        #Used for extreme rows that are included in every test done
        self.ois_query_string = None
        elements = io_info_element.getElementsByTagName('outlier_inc_set')
        if len(elements) > 0 :
            ois_elem = elements[0] 
            if len(ois_elem.getElementsByTagName('or')) > 0:
                self.ois_query_string = self.util_create_query_string(ois_elem)

        #Getting x/y boundaries of the parcels and number of rows 
        #(may want to find a faster way to do this)
        (self.x_max, self.y_max, self.x_min, self.y_min, self.total_count) = self.util_spatial_boundaries() 
        
        self.rows_left = self.total_count

        #Information that is being stored about the number of parcel blocks remaining and used
        self.printOut.pLog("RET- Creating all parcel blocks...")
            
            
        self.block_list = self.util_create_parcel_block(self.x_max, self.y_max, self.x_min, self.y_min) 
        self.set_colors()
        self.used_blocks = []
        
        #In order to make sure max, min vals didn't leave any out
        #Can happen if x and y attributes are varchars in metadata
        self.adjust_borders()
        
        #Used for profiling the speed at which the program is running
        self.first_query_time = None
        self.number_rows_tested = 0
        
        self.table_current_test_rows = []

        #Parcel block information
        self.current_test_block = None
        self.current_training_block = None
        self.group_max = 2
        self.group_count = 2
        if io_info_element.hasAttribute('num_cv_folds') :
            self.group_max = int(io_info_element.attributes['num_cv_folds'].value)
            self.group_count = self.group_max

        self.overall_is_test_list = []
        self.use_as_training = []

        #Current rows retrieved
        self.current_rows = []
        self.is_test_list = []
        self.is_null_list = []
        self.test_number = []

    #Gets rows that represent a block of parcels
    #Returns None if there aren't any rows left
    def query_rows(self) :

        #FOR GUI
        self.printOut.progress(int((self.rows_left / float(self.total_count))*100))

        #Getting all new data loaded in data structures
        if self.group_count == self.group_max :

            #Reset the group count
            self.group_count = 1

            #Profiling (won't work if distributed) ############
            #Getting information about approximate time left
            if self.first_query_time == None :
                self.first_query_time = time.time()
            else :
                average_time = (time.time() - self.first_query_time) / (self.number_rows_tested)
                
                self.printOut.pLog( "PROFILE- Number of blocks remaining: " + str(len(self.block_list)))
                self.printOut.pLog( "PROFILE- Average time per unit: " +  str(average_time))
                self.printOut.pLog( "PROFILE- Number of rows remaining: " + str(self.rows_left))
                self.printOut.pLog( "PROFILE- Predicted remaining time (in minutes): " + str(int((average_time*(self.rows_left))/60)))
    
            ####################################################
            
            self.printOut.pLog( "RET- Retrieving training and test parcels from remaining: " + str(self.rows_left))      
            
            #Getting a block with a non zero parcel count
            block = None
            while self.block_list != [] and block == None :
                block = self.block_list.pop(0)
                if block.parcel_count == 0 :
                    block = None
    
            if block != None :
                
                self.current_test_block = block                
                training_rows_query = self.util_training_rows(block)
                
                start_time = int(time.time())
                
                #Getting the attribute values from the raw rows
                #Get rows into the proper format
                proper_rows = []            
                id_set = set([])
                for row in training_rows_query :
                    temp_row = {}
                    for attribute in self.attributes :
                        temp_row[attribute] = row[attribute]                                        
                    proper_rows.append(temp_row)
                    id_set.add(row[self.id_attribute])
        
                #Getting test and training rows (test is a subset of training)
                is_test_list = []
                test_number = []
                test_count = 0
                for index in range(len(proper_rows)) :
                    row = proper_rows[index]
    
                    #REQUIRES X and Y attributes to be included in the rows (may be a problem)
                    if block.row_within_block(self.x_attribute, self.y_attribute, row) :
                        is_test_list.append(True)
                        test_number.append(test_count)
                        test_count += 1
                    else :
                        is_test_list.append(False)
                        test_number.append(None)
                
                #Adjust block count (cause borders are modified in some cases)
                block.parcel_count = test_count
                
                self.used_blocks.append(block)
                self.rows_left -= block.parcel_count
                self.number_rows_tested += block.parcel_count
    
                #Adding the extreme values that need to be added to every data set
                #This helps outlier detection and null value predictions
                if self.ois_query_string != None :
                    s = self.table.select(and_(self.ois_query_string, self.query_string )).execute()
                    self.printOut.pLog( "RET- Num extra (rare) rows added: " + str(s.rowcount))
                    for row in s :
                        if row[self.id_attribute] not in id_set :
                            temp_row = {}
                            for attribute in self.attributes :
                                temp_row[attribute] = row[attribute]                                        
                            
                            proper_rows.append(temp_row)
                            is_test_list.append(False)
                            test_number.append(None)
    
                self.current_rows = proper_rows
                self.is_test_list = is_test_list
                self.overall_is_test_list = copy.deepcopy(is_test_list)
                self.test_number = test_number
    
                end_time = int(time.time())
                self.printOut.pLog( "RET- Time loading data structures: " + str(end_time - start_time))
    
            else :
                self.current_rows = []
                self.is_test_list = []
                self.test_number = []

                self.overall_is_test_list = []
                self.use_as_training = []

        #Increment group count
        else :
            self.group_count += 1

        #Use data that exists / loading temporary data structures
        self.is_test_list = []
        self.use_as_training = []

        test_num = 0
        test_count = 0
        train_count = 0

        #Going over every current row
        for index in range(len(self.current_rows)) :
            #if ONE group then all in test
            if self.group_max == 1 :
                if self.overall_is_test_list[index] :
                    self.is_test_list.append(True)
                    test_count += 1
                else :
                    self.is_test_list.append(False)
                    
                self.use_as_training.append(True)
                train_count += 1
            
            #If more than one group then split up test and training sets
            else :
                is_test = self.overall_is_test_list[index]
                if is_test :
                    test_num += 1
    
                #Deciding whether instance will be in the test set
                #Splits test set up
                #MISSING 4 VALUES IN SANITY CHECK
                used_as_test = False
                if is_test and test_num % self.group_max == (self.group_count - 1) : 
                    self.is_test_list.append(True)
                    used_as_test = True
                    test_count += 1
    
                else :
                    self.is_test_list.append(False)
                
                #Deciding whether instance should be a training data set
                #FIND INTELIGENT WAY TO STOP THE TRAINING SET FROM BEING TO LARGE
                if not used_as_test :
                    train_count += 1
                    
                if not used_as_test :
                    self.use_as_training.append(True)
                else :
                    self.use_as_training.append(False)

        self.printOut.pLog( "RET- Group: " + str(self.group_count))
        self.printOut.pLog( "RET- Test count: " + str(test_count))
        self.printOut.pLog( "RET- Train count: " + str(train_count))

    #Returns the number of rows that are left
    #to be retrieved
    def number_remaining_blocks(self) :
        if len(self.block_list) == 0 and self.group_count == self.group_max :
            return 0
        else :
            return 1


    #Used to setup basic query string
    def util_create_query_string(self, element):
        
        #Getting dictionary of column objects
        #Creating and clauses for all columns in test criteria combined
        qs = True
        and_list = []
        for or_tag in element.getElementsByTagName('or') :
            
            #Creating or clauses for a given "or list"
            or_list = []
            for elem in or_tag.getElementsByTagName('tc') :
                attribute = elem.attributes['attribute'].value
                type = elem.attributes['type'].value
                value = elem.attributes['value'].value

                #Getting the right form of the value
                vt = elem.attributes['vt'].value
                if vt == "string" :
                    value = str(value)
                elif vt == "int" :
                    value = int(value)
                
                #Creating clause for criteria
                if type == "E" :       
                    or_list.append(self.table.c[attribute] == value)
                elif type == "NE" :
                    or_list.append(self.table.c[attribute] != value)
                elif type == "GT" :
                    or_list.append(self.table.c[attribute] > value)
                elif type == "LT" :
                    or_list.append(self.table.c[attribute] < value)

            if len(or_list) > 0 :
                and_list.append(or_(*or_list))

        #Only make the query string equal to the list if there is something in the list
        if len(and_list) > 0 :   
            qs = and_(*and_list)

        return qs

    #util                                                                                               
    #keeps track of all parcel blocks                                                                         
    class Parcel_block :
        def __init__(self, x_max, y_max, x_min, y_min, parcel_count) :
            self.x_max = float(x_max)
            self.y_max = float(y_max)
            self.x_min = float(x_min)
            self.y_min = float(y_min)
            self.parcel_count = parcel_count
            
            self.right_border = False
            self.bottom_border = False
            
            #For visual represantation
            self.color = None
                        
        #Sets values for whether sides are borders
        def set_border_bools(self, query_manager):
            if self.y_min == query_manager.y_min :
                self.bottom_border = True
            if self.x_max == query_manager.x_max :
                self.right_border = True
            
        def row_within_block(self, x_at, y_at, row) :
            #There are strict equalties for the lower and right sides of the block
            #UNLESS that side borders the edge of space
            xa = float(row[x_at])
            ya = float(row[y_at])
            rb = self.right_border
            bb = self.bottom_border
            
            if xa >= self.x_min and ((rb and xa <= self.x_max) or (not rb and xa < self.x_max)) :
                if ya <= self.y_max and ((bb and ya >= self.y_min) or (not bb and ya > self.y_min)):
                    return True

            return False

    #util
    #Gets all the training rows (super set of test rows)
    def util_training_rows(self, block) :
        (cx_max, cy_max, cx_min, cy_min) = [block.x_max, block.y_max, block.x_min, block.y_min] 
        current_count = block.parcel_count

        if current_count == 0 :
            return [[], []]
        else :
            self.printOut.pLog( "RET- Current count inside training block: " + str(current_count))

            #setting easy variables
            x = self.x_attribute
            y = self.y_attribute
            t = self.table

            #ROOM FOR IMPROVEMENT
            #Make it so that this doesn't terribly overshoot the training size
            count_repeated = 0
            last_count = 0
            select_stat = t.select(and_(t.c[x] >= cx_min, t.c[x] <= cx_max, t.c[y] >= cy_min, t.c[y] <= cy_max, self.query_string ))
            while(current_count < self.train_size) :
                change = math.sqrt((self.train_size - current_count) / float(max(self.train_size/10, current_count)))
                cx_min -= (cx_max - cx_min)*change*.1 
                cx_max += (cx_max - cx_min)*change*.1
                cy_min -= (cy_max - cy_min)*change*.1
                cy_max += (cy_max - cy_min)*change*.1
                             
                select_stat = t.select(and_(t.c[x] >= cx_min, t.c[x] <= cx_max, t.c[y] >= cy_min, t.c[y] <= cy_max, self.query_string ))
                
                #Getting the number of instances inside the block
                s = select([func.count("*")], and_(t.c[x] >= cx_min, t.c[x] <= cx_max, t.c[y] >= cy_min, t.c[y] <= cy_max, self.query_string ), from_obj=[t]).execute()
                block_count = parcel_count = sql_get_agg(s, "int")             
                
                last_count = current_count
                current_count = block_count
                
                self.printOut.pLog( "RET- Current count inside training block: " + str(current_count))
                          
                #Protects against cases in which current_count will never be bigger than train_size
                if last_count == current_count :
                    count_repeated += 1
                else :
                    count_repeated = 0
                if count_repeated == 5 :
                    break
            
            #Executing the training query
            s = select_stat.execute()
            
            #Used for parcel visual
            self.current_training_block = self.Parcel_block(cx_max, cy_max, cx_min, cy_min, "(training block)")
            self.current_training_block.color = self.current_test_block.color
            
            return s
         
    #util
    #Seperates parcels in a grid type fashion and creates
    #spatial objects for each grid
    def util_create_parcel_block(self, tx_max, ty_max, tx_min, ty_min) :
        t = self.table
        x = self.x_attribute
        y = self.y_attribute

        #NEED TO BE IMPROVED
        #The inequalities should be made strict in a certain way in order to insure nothings redundant
        s = select([func.count("*")], and_(t.c[x] >= tx_min, t.c[x] <= tx_max, t.c[y] >= ty_min, t.c[y] <= ty_max, self.query_string ), from_obj=[t]).execute()
        parcel_count = sql_get_agg(s, "int")

        #ROOM FOR IMPROVEMENT
        #Make it so that very small test blocks aren't created
        if parcel_count > self.test_size :
            x_mid = (tx_max - tx_min) / 2 + tx_min
            y_mid = (ty_max - ty_min) /2 + ty_min
            
            temp_list = []
            
            #Always splits in such a way that the the resulting rectangles are squarish
            x_diff = tx_max - tx_min
            y_diff = ty_max - ty_min
            if x_diff < y_diff :
                #Split horiz
                temp_list.extend(self.util_create_parcel_block(tx_max, ty_max, tx_min, y_mid))
                temp_list.extend(self.util_create_parcel_block(tx_max, y_mid, tx_min, ty_min))
            else :
                #Split vert
                temp_list.extend(self.util_create_parcel_block(tx_max, ty_max, x_mid, ty_min))
                temp_list.extend(self.util_create_parcel_block(x_mid, ty_max, tx_min, ty_min))
                
            return temp_list
        else :
            p = self.Parcel_block(tx_max, ty_max, tx_min, ty_min, parcel_count)
            self.printOut.pLog( "RET- Block size: " + str(parcel_count))

            p.set_border_bools(self)
            return [p]

    #util
    #Returns the max and min x and y coordinate values
    def util_spatial_boundaries(self) :
        self.printOut.pLog( "RET- Finding spatial boundaries of the database...")
    
        t = self.table
    
        #Setting overall values
        (x_max, y_max, x_min, y_min) = [None, None, None, None]
        s = select([func.count("*")], self.query_string, from_obj=[t]).execute()
        total_count = sql_get_agg(s, "int")

        s = select([func.max(t.c[self.x_attribute])]).execute()
        x_max = sql_get_agg(s, "float")
        
        s = select([func.min(t.c[self.x_attribute])]).execute()
        x_min = sql_get_agg(s, "float")
        
        s = select([func.max(t.c[self.y_attribute])]).execute()
        y_max = sql_get_agg(s, "float")
        
        s = select([func.min(t.c[self.y_attribute])]).execute()
        y_min = sql_get_agg(s, "float")

        return [x_max, y_max, x_min, y_min, total_count]
    
    #Creates a list that says whether each value is null or not
    def proc_is_null_list(self, test_object) :
        self.printOut.pLog( "RET- Test Attribute: " + str(test_object.test_attribute))

        is_null_list = [] 
        for i in range(len(self.current_rows)) :
            is_null = False
            for null_dict in test_object.null_value_list :

                value = null_dict["value"]
                type = null_dict["type"]
                row_value = self.current_rows[i][null_dict["attribute"]]
                
                if type == "GT" and row_value > value :
                    is_null = True
                    break
                elif type == "LT" and row_value < value :
                    is_null = True
                    break
                elif type == "E" and row_value == value :
                    is_null = True
                    break
                elif type == "NE" and row_value != value :
                    is_null = True
                    break

            is_null_list.append(is_null)
            
        self.is_null_list = is_null_list
        self.printOut.pLog( "RET- Found " + str(is_null_list.count(True)) + " null labels in whole training blocks")
            

    #makes it so class and num attribute lists only represent attributes being used in tests
    def update_att_lists(self, model_list):
        new_class_list = []
        new_num_list = []
        
        self.printOut.pLog( "RET- Checking that all needed attributes are in the table.")
        
        #finding all attributes being used
        for model in model_list :
            for attribute in model.attributes :
                if attribute in self.class_list :
                    new_class_list.append(attribute)
                elif attribute in self.numeric_list :
                    new_num_list.append(attribute)
                else :
                    self.printOut.pLog( "ERROR: Attribute Not in table- " + attribute)
            
            #Make sure the target attribute is included
            if model.test_attribute in self.class_list :
                new_class_list.append(model.test_attribute)
            elif model.test_attribute in self.numeric_list :
                new_num_list.append(model.test_attribute)
            elif model.test_attribute != None :
                self.printOut.pLog( "ERROR: Target Attribute Not in Table- ", model.test_attribute)

        self.printOut.pLog( "")
        
        self.class_list = new_class_list
        self.numeric_list = new_num_list

    #Finds color for each block
    #(Uses modified color scheme)
    def set_colors(self):
        color_list = ["red", "blue", "green", "yellow"]
        #Recording all touching blocks
        blocks_touching ={}
        for block in self.block_list :
            blocks_touching[block] = set([])
            #Checking which blocks are touching
            for ob in self.block_list :
                #left or right
                if block.x_min == ob.x_max or block.x_max == ob.x_min :
                    if not block.y_max <= ob.y_min and not block.y_min >= ob.y_max :
                        blocks_touching[block].add(ob)
                #top or bottom      
                elif block.y_min == ob.y_max or block.y_max == ob.y_min :
                    if not block.x_max <= ob.x_min and not block.x_min >= ob.x_max :
                        blocks_touching[block].add(ob)
        
        #Randomly coloring blocks
        #but making sure as many conflicts can be avoided as possible
        conflict_count = 0
        for block in self.block_list :
            available_colors = copy.deepcopy(color_list)
            for nb in blocks_touching[block] :
                if nb.color in available_colors :
                    available_colors.remove(nb.color)
    
            if len(available_colors) > 0 :
                #Picking a color that a neighbor doesn't have
                index = random.randint(0, len(available_colors) - 1)
                block.color = available_colors[index]
            else :
                #Picking a random color
                index = random.randint(0, len(color_list) - 1)
                block.color = color_list[index]
                conflict_count += 1
        self.printOut.pLog( "RET- Color conflicts: " + str(conflict_count)) 
        
    #For cases in which location variables are strings (in the database)    
    def adjust_borders(self):
        
        new_x_max = round_up(self.x_max)        
        new_x_min = round_down(self.x_min)
        new_y_max = round_up(self.y_max)
        new_y_min = round_down(self.y_min)
        
        for block in self.block_list :
            if block.x_max == self.x_max :
                block.x_max = new_x_max
            if block.y_max == self.y_max :
                block.y_max = new_y_max
            if block.x_min == self.x_min :
                block.x_min = new_x_min
            if block.y_min == self.y_min :
                block.y_min = new_y_min
        
        self.x_max = new_x_max
        self.y_max = new_y_max
        self.x_min = new_x_min
        self.y_min = new_y_min        
        
#UTIL Functions        

#Made up round up / down functions
def round_up(val):
    if val < 0 :
        new_val = round_down(-1.0*val)
        return -1.0*new_val
    else :
        mult = pow(10, NUMBER_DIGITS_ROUND)
        new_val = (int(val*mult) + 1) / float(mult)
        return new_val    
      
def round_down(val):
    if val < 0 :
        new_val = round_up(-1.0*val)
        return -1.0*new_val
    else :
        mult = pow(10, NUMBER_DIGITS_ROUND)
        new_val = int(val*mult) / float(mult)
        return new_val
 
#Gets information about the columns
def util_get_attribute_info(table, forced_class_att_list, forced_num_att_list ):

    attributes = []
    class_list = []
    numeric_list = []
    
    #Loop over all columns and figure out what there types are
    for column in table.columns :
        data_type = str( column.type )
        name = column.name
        
        attributes.append(name)

        #Forcing some columns to be class attributes
        if name in forced_class_att_list :
            class_list.append(name)
        #Forcing some columns to be numeric attributes
        elif name in forced_num_att_list :
            numeric_list.append(name)
        #Finding columns that are a class type (may exclude PK, might not work)
        elif data_type.find("MSDouble") == -1 and data_type.find("MSInteger" ) == -1 and data_type.find("MSDecimal") == -1 :
            class_list.append(name)
        #Finding columns that are numeric type
        else :
            numeric_list.append(name)

    return [class_list, numeric_list, attributes]

#Gets attributes from a string        
def util_get_attribute_list(string):
    initial_list = string.split(",")
    
    list = []
    for attribute in initial_list :
        new = attribute.rstrip(" ")
        new = new.lstrip(" ")
        list.append(str(new))

    return list
  
#util function
def util_get_table(db_url, table_name) :
    #Get SQL connection                                                                                     
    db = create_engine(db_url)
    metadata = MetaData(db)

    #Get the table that is being inspected                                                        
    t = Table(table_name, metadata, autoload=True)
    return t

#Returns the value for a count, max, min, etc.
def sql_get_agg(s, type):
    for row in s :
        if type == "int" :
            return int(row[0])
        elif type == "float" :
            return float(row[0])
    
