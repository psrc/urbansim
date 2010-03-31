from xml.dom import minidom
import copy
import time, sys, os

import MySQLdb
from sqlalchemy import *

from data_handler.data_retrieval import Query_manager
from data_handler.data_preparation import Data_profiler
from output.generic_output import Output_manager
from models.ldof_model import LDOF_model

#loads system variables
path = os.environ.get('OPUS_HOME')
path = os.path.join(path, "src", "data_mining", "SYSTEM_VARIABLES.py")
execfile(path) 

#Runs all the tests
def run_test(xml_config_address, logCB=None, progressCB=None, usingConfig=True) :
    
    start = time.time()
    
    #Load the xml_configuration file and pass the database information to a Query_manager
    xmldoc = xml_config_address
    if usingConfig :
        xmldoc = minidom.parse(xml_config_address)
    
    #Loading tests from xml file
    model_info = xmldoc.getElementsByTagName('model_info')[0]
    model = LDOF_model(model_info, logCB, progressCB)
        
    #Setting up query manager
    io_info = xmldoc.getElementsByTagName('io_info')[0]
    query_manager = Query_manager(io_info, logCB, progressCB)
    query_manager.update_att_lists([model])
    query_manager.group_max = 1
    query_manager.group_count = 1
    
    #Pick a random target_attribute (it isn't used so it doesn't matter)
    #WILL THROW ERROR IF NO NUMERIC ATTRIBUTES ARE USED
    model.test_attribute = query_manager.numeric_list[0]
    
    #Setting up output table

    #Add extra columns to view if supported
    extra_columns = []
    if io_info.hasAttribute('extra_attributes') :
        extra_columns = util_get_attribute_list(io_info.attributes['extra_attributes'].value)

    columns_list = get_columns_list(query_manager, model.attributes, extra_columns, model)
    output_manager = Output_manager(io_info, None, columns_list)
    
    #Impute values for all rows for each block
    while(query_manager.number_remaining_blocks() > 0) :
        
        query_manager.query_rows()
        
        #Making sure there are some test rows in the blocked set of query rows
        if query_manager.is_test_list.count(True) > 0 :                    
            
            #Get ranges of values for all the columns in the queried rows            
            data_profiler = Data_profiler(query_manager)
            
            #Setup the data that is going to be used for the test
            data_profiler.prepare_test_data(model)
                                
            #Making predictions for a given attribute
            test_result = model.get_predictions(data_profiler)
                    
            #Updating null values
            update_rows(query_manager, data_profiler, test_result, model)
         
            #Add rows to the new table (only addition is the ldof value)
            test_rows = []
            for i in range(len(query_manager.current_rows)) :
                if query_manager.is_test_list[i] :
                    test_rows.append(query_manager.current_rows[i])
                    
            output_manager.insert_rows(test_rows)
          
    #Posting information about time taken 
    end = time.time()
    print "Overall Time taken: ", int(end - start)
    if logCB != None :
        logCB("Overall Time taken: " + str(int(end - start)))
    return 0


########### Utility Scripts ######################

#Add all ldof values to the row
def update_rows(query_manager, data_profiler, test_result_obj, ldof_model):
    
    #Get actual id mapping
    #Relies on the fact that all instances in the training block are used
    #for training (since there are no null value tags)
    id_map = []
    for index in range(len(query_manager.current_rows)) :
        id_map.append(query_manager.current_rows[index][query_manager.id_attribute])
    
    #Change this eventually
    test_count = 0
    
    for i in range(len(query_manager.current_rows)) :
        
        #Keeping track of test_count
        if query_manager.is_test_list[i] :
                
            #updating lof values
            k = ldof_model.k
            for v in test_result_obj.lof_lists[test_count] :
                av = float("%.2f" % v)
                query_manager.current_rows[i]["lof" + str(k)] = av
                k -= ldof_model.num_mod

            #updating lof id values
            k = ldof_model.k
            for v in test_result_obj.lof_id_lists[test_count] :
                av = unicode(id_map[int(v)])
                query_manager.current_rows[i]["lof" + str(k) + "_id"] = av
                k -= ldof_model.num_mod

            test_count += 1

        
#Getting columns that are going to be added to the output table
def get_columns_list(query_manager, attributes, extra_attributes, ldof_model):
    column_list = []
 
     #Getting the columns from the table passed to the query manager
    for c in query_manager.table.columns :
        if c.name in extra_attributes and c.name not in attributes: #For now only include attributes used for the test
            column_list.append(c.copy())
    
    #Getting the columns from the table passed to the query manager
    for c in query_manager.table.columns :
        if c.name in attributes : #For now only include attributes used for the test
            column_list.append(c.copy())
        
    #Columns that keep track of lof
    for k in range(ldof_model.k):
        i = k + 1
        if i % ldof_model.num_mod == 0 :
            c = Column("lof" + str(i), Numeric, nullable=True)
            column_list.append(c)
    
    #Columns that keep track of the neighbors
    for k in range(ldof_model.k):
        i = k + 1
        if i % ldof_model.num_mod == 0 :
            c = Column("lof" + str(i) + "_id", UnicodeText(11), nullable=True)
            column_list.append(c)
    
    return column_list

#Gets attributes from a string        
def util_get_attribute_list(string):
    initial_list = string.split(",")
    
    list = []
    for attribute in initial_list :
        new = attribute.rstrip(" ")
        new = new.lstrip(" ")
        list.append(str(new))

    return list   

#Just for testing at the moment
if not USING_GUI :
    run_test(sys.argv[1])
