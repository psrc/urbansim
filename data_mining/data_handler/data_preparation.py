import copy
import math
import time
import os

try: import MySQLdb
except: pass
from sqlalchemy import *
import numpy
from data_mining.PrintOutput import PrintOutput

from opus_core import paths


#loads system variables                                                                                  
path = paths.get_opus_home_path("src", "data_mining", "SYSTEM_VARIABLES.py")
exec(compile(open(path, "rb").read(), path, 'exec')) 

#Keeps track of information about the current data
class Data_profiler :

    def __init__(self, query_manager, logCB = None, progressCB = None) :
        
        #For reporting results
        self.printOut = PrintOutput(logCB, progressCB, PROFILING)        


        self.query_manager = query_manager

        #Profile of information currently being dealt with
        self.class_result_dict = None
        self.class_att_value_weight = None
        self.numeric_result_dict = None
        self.get_possible_values(query_manager)
        
        #Used by SVM_model to piece together results
        self.label_id_lookup_table = None
        
        #Current data being stored
        self.labels = []
        self.samples = []
        self.is_null_list = []
        
        #Used by KNN
        self.log_trans_atts = set([])
        self.attribute_id_list = []
        self.attribute_id_dict = {}
        self.id_attribute_dict = {}

    #util function
    #creates dictionary of possible values for each column in the table
    def get_possible_values(self, query_manager) :
    
        #Getting info from the query manager
        class_list = query_manager.class_list
        numeric_list = query_manager.numeric_list
        rows = query_manager.current_rows
    
        start_time = int(time.time())
        self.printOut.pLog("PREP- Class columns count: " + str(len(class_list)))
        self.printOut.pLog("PREP- Num columns count: " + str(len(numeric_list)))
    
        #Initializing data structures for storing info
        class_result_dict = {}
        class_att_value_count = {}
        numeric_result_dict = {}
        for c in class_list :
            class_result_dict[c] = []
            class_att_value_count[c] = {}
        for c in numeric_list :
            numeric_result_dict[c] = [None, None]
    
        #Finding all possible values for each column
        for row in rows :
    
            #gathering class info
            for c_name, list in class_result_dict.items() :
                if c_name in row :
                    value = row[c_name]
        
                    #Getting information on class attribute values
                    if value not in list :
                        list.append(value)
                        class_att_value_count[c_name][value] = 1 #May need to worry about the value being Null
                    else :
                        class_att_value_count[c_name][value] += 1
        
            #gathering numeric info
            for c_name, list in numeric_result_dict.items() :
                if c_name in row :
                    
                    value = row[c_name]
                    if value == "" or value == None:
                        value = 0 #May want to think of a more appropriate value
                    else :
                        value = float( value )
        
                    #finding min
                    if value != "" and (list[0] > value or list[0] == None ) :
                        list[0] = value
                    
                    #finding max
                    if value != "" and (list[1] < value or list[1] == None) :
                        list[1] = value
    
        #Deciding on the weight based on the count
        class_att_value_weight = {}
        for att_name, values in class_att_value_count.items() :
            #Finding total number of values
            overall_count = 0
            for value, count in values.items() :
                overall_count += count
            
            #Setting weights
            class_att_value_weight[att_name] = {}
            for value, count in values.items() :
                class_att_value_weight[att_name][value] = float(count / overall_count)
            
            
        self.numeric_result_dict = numeric_result_dict
        self.class_result_dict = class_result_dict
        self.class_att_value_weight = class_att_value_weight
    
        end_time = int(time.time())
        self.printOut.pLog("PREP- Time getting values: " + str(end_time - start_time))
    
    #Prepares the data that will be used with SVM or KNN
    def load_data_structures(self, target, attributes) :
    
        start_time = int(time.time())
    
        #Getting list of columns, but making sure the columns are actually there
        column_list_local = []
        for attribute in attributes :
            if attribute in self.class_result_dict or attribute in self.numeric_result_dict :
                column_list_local.append(attribute)
        
        (class_lookup_table, id_lookup_table)  = self.util_get_class_lookup_table()
        
        self.label_id_lookup_table = id_lookup_table #Used by SVM to piece together test results
        self.class_lookup_table = class_lookup_table #Used by SVM to piece together test results
    
        labels = []
        samples = []
        
        #Getting all needed information from all rows
        for j in range(len(self.query_manager.current_rows)) :
            
            row = self.query_manager.current_rows[j]
            
            #for class target attributes
            value = row[target]
            if target in class_lookup_table :
                labels.append(class_lookup_table[target][value])
        
            #for numeric target attributes (might want to scale label)
            else :
                if value == "" or value == None:
                    value = -1
                labels.append(int( value )) #CHANGE: SHOULD BE FLOAT
        
            #getting sample data
            index = 0
            sample = {}
            for attribute in column_list_local :
                if attribute in row :
                    if attribute in class_lookup_table :
                        value = row[attribute]
                        attribute_value = class_lookup_table[attribute][value]
                            
                        for i in range( len( self.class_result_dict[attribute] ) ) :
                            if attribute_value == i :
                                #sample[index] = 0.5 #1
                                sample[index] = self.class_att_value_weight[attribute][value] #MAKE IT ONLY FOR LDOF
                                
                            index += 1
                            
                    elif attribute in self.numeric_result_dict :
                        value = row[attribute]
                        if value == "" or value == None:
                            value = 0
            
                        scaled = 0
                        max = self.numeric_result_dict[attribute][1]
                        min = self.numeric_result_dict[attribute][0]
            
                        #Transforming specified columns
                        if attribute in self.log_trans_atts :
                            value = math.log(value + 1)
                                
                            #Scaling values
                            denominator = math.log(max + 1) - math.log(min + 1)
                            if denominator > 0 :
                                    
                                #Scaling all attributes between 0 and 1
                                numerator = float( value ) - math.log(min + 1)
                                scaled =  numerator / denominator
                                                
                        else :
                                
                            #Non transformed columns
                            #Scaling values
                            denominator = max - min
                            if denominator > 0 :
                                    
                                #Scaling all attributes between 0 and 1
                                numerator = float( value ) - min
                                scaled =  numerator / denominator
                                    
                                
                        sample[index] = scaled
                        index += 1 
    
            samples.append(sample)
    
        #Used for KNN
        self.printOut.pLog( "PREP- Dimension / column mapping")

        self.attribute_id_dict = {}
        self.id_attribute_dict = {}
        self.attribute_id_list = []
        id = 0
        for attribute in column_list_local :
            self.printOut.pLog( "PREP- ID: " + str(id) + ", Attribute: " + attribute)
        
            if attribute in class_lookup_table :
                for att_value in list(class_lookup_table[attribute].keys()) :
                    self.attribute_id_list.append(id)
                self.attribute_id_dict[id] = attribute
                self.id_attribute_dict[attribute] = id 
            else :
                self.attribute_id_dict[id] = attribute
                self.id_attribute_dict[attribute] = id
                self.attribute_id_list.append(id)
            id += 1
            
        #Setting values for object variables / lists
        self.labels = labels
        self.samples = samples
    
        end_time = int(time.time())
        self.printOut.pLog("PREP- Time loading data structures: " + str( end_time - start_time))
       
    #Setting up all the data for the test
    def prepare_test_data(self, test_object) : 
        
        #Making the data in the data profiler formatted correctly for the
        #Given test attribute and attributes used for the test           
        self.load_data_structures(test_object.test_attribute, test_object.attributes)

        #Setting transformation information in data profiler
        #only do this for KNN attributes
        if test_object.test_type == "KNN" :
            self.log_trans_atts = set(test_object.log_trans_atts)
    
        #Processing information about which rows are null
        self.query_manager.proc_is_null_list(test_object)
    
    
    #util function
    def util_get_class_lookup_table(self) :
        class_lookup_table = {}
        id_lookup_table = {}
        for class_name, values in self.class_result_dict.items() :
            index = 0
            class_temp = {}
            id_temp = {}
            for value in values :
                class_temp[value] = index
                id_temp[index] = value
                index += 1
            class_lookup_table[class_name] = class_temp
            id_lookup_table[class_name] = id_temp
    
        return [class_lookup_table, id_lookup_table]        

#util function                                                                                                                                           
def get_table(db_url, table_name) :
    #Get SQL connection                                                                                                                                                 
    db = create_engine(db_url)
    metadata = MetaData(db)

    #Get the table that is being inspected                                                                                                                               
    t = Table(table_name, metadata, autoload=True)
    return t
