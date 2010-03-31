from xml.dom import minidom
import copy
import time
import sys
import os
import subprocess

import MySQLdb
from sqlalchemy import *

from data_handler.data_retrieval import Query_manager
from data_handler.data_preparation import Data_profiler
from output.generic_output import Output_manager
from output.log_output import Log_manager
from models.weka_num_model import Num_model
from models.weka_cat_model import Cat_model

#loads system variables
path = os.environ.get('OPUS_HOME')
path = os.path.join(path, "src", "data_mining", "SYSTEM_VARIABLES.py")
execfile(path) 

#Checking if pygame has been installed
use_drawing = True
try :
    from output.visual_output import Parcel_block_vis
except ImportError :
    use_drawing = False
use_drawing = use_drawing and DRAW_BLOCKS

#Runs all the tests
def run_test(xml_config_address, logCB=None, progressCB=None, usingConfig=True) :
    
    start_time = time.time()
    
    #Load the xml_configuration file and pass the database information to a Query_manager
    xmldoc = xml_config_address
    if usingConfig :
        xmldoc = minidom.parse(xml_config_address)
    io_info = xmldoc.getElementsByTagName('io_info')[0]

    #Seeing whether to display all predictions
    MAKE_ALL_PREDS = False
    if io_info.hasAttribute('display_all_predictions') :
        MAKE_ALL_PREDS = str(io_info.attributes['display_all_predictions'].value) == 'True'   
    
    #Loading tests from xml file
    model_info_list = xmldoc.getElementsByTagName('model_info')
    model_list = []
    for model_info in model_info_list :
        
        type = model_info.attributes["type"].value
        if type == "Num" :
            model_list.append(Num_model(model_info, MAKE_ALL_PREDS, logCB, progressCB))
        elif type == "Cat" :
            model_list.append(Cat_model(model_info, MAKE_ALL_PREDS, logCB, progressCB))
    
    #Setting up query manager
    query_manager = Query_manager(io_info, logCB, progressCB)
    query_manager.update_att_lists(model_list)
        
    #Setting up output table
    columns_list = get_columns_list(query_manager, model_list, MAKE_ALL_PREDS)
    if io_info.hasAttribute("output_table_name") :
        output_manager = Output_manager(io_info, None, columns_list)
        if output_manager.table == None :
            print "ERROR: ordered not to overwrite table, but existing table is uncompatible with current test"
            return -1
    else :
        output_manager = Output_manager(None, query_manager, columns_list)
    
    #Settting up output log (NOT USED IF TAG doesn't exist)
    log_manager = None
    if io_info.hasAttribute("log_folder_address") :  
        log_manager = Log_manager(io_info, xml_config_address)
        if log_manager.folder_address == None :
            print "ERROR: ordered to not overide the log folder and a log folder exists"
            return -1
    
    #Setting up parcel drawer
    if use_drawing :
        parcel_block_vis = Parcel_block_vis(query_manager, query_manager.table_name)

    #Keeping track of tests that are actually run
    ran_test = {}
    for model in model_list :
        ran_test[model] = False
    
    #Impute values for all rows for each block
    while(query_manager.number_remaining_blocks() > 0) :
        
        query_manager.query_rows()
        
        #Making sure there are some test rows in the blocked set of query rows
        if query_manager.is_test_list.count(True) > 0 :
            
            #When all predictions are made none of the original values will be changed
            if not MAKE_ALL_PREDS :
                
                #Initialize data imputed columns for each row
                for row in query_manager.current_rows :
                    for model in model_list :
                        row[model.test_attribute + "_imputed"] = 0
                            
                                        
            #Running all given tests
            for model in model_list :
                            
                #Making predictions for a given attribute
                test_result = model.get_predictions(query_manager)

                #Updating null values
                if test_result != None :
                    ran_test[model] = True
                    update_rows(query_manager, test_result, MAKE_ALL_PREDS)
         
                    #Recording accuracy estimation
                    if log_manager != None :
                        log_manager.get_block_stats(query_manager, test_result)
         
            #Replace null values in data, and update imputed columns
            #Only add test rows, not training rows (list of rows that will be added)
            test_rows = []
            for i in range(len(query_manager.current_rows)) :
                if query_manager.is_test_list[i] :
                    test_rows.append(query_manager.current_rows[i])
                    
            output_manager.insert_rows(test_rows)
          
            #Record parcels visually
            if use_drawing :
                parcel_block_vis.print_parcels(query_manager)
            
    #Close parcel block visual
    if use_drawing and log_manager != None :
        parcel_block_vis.close_image(log_manager)
    
    #Print all log information to logs
    if log_manager != None :
        log_manager.store_stats(query_manager, output_manager, model_list, start_time, ran_test) 
            
    #Posting information about time taken 
    end_time = time.time()
    print "Overall Time taken: ", int(end_time - start_time)
    if logCB != None :
        logCB("Overall Time taken: " + str(int(end_time - start_time)))
        
    return 0


########### Utility Functions ######################

#Replaces all null values with prediction, and updates imputed column
def update_rows(query_manager, test_result_obj, MAKE_ALL_PREDS):
    
    #Change this eventually
    test_count = -1        
        
    #Local info
    block_num = test_result_obj.accuracy_estimation["block number"]
                                                
    for i in range(len(query_manager.current_rows)) :
            
        #Keeping track of test_count
        if query_manager.is_test_list[i] :
            test_count += 1
            
        #Finding rows that are null and test rows
        if query_manager.is_test_list[i] and (query_manager.is_null_list[i] or MAKE_ALL_PREDS):
            att = test_result_obj.test_attribute
                
            #Only replaces null values
            if not MAKE_ALL_PREDS :
                query_manager.current_rows[i][att] = test_result_obj.prediction_list[test_count]
                query_manager.current_rows[i][att + "_imputed"] = 1
            else :
                query_manager.current_rows[i][att + "_new"] = test_result_obj.prediction_list[test_count]
                query_manager.current_rows[i]["block_num"] = block_num
                                    
#Getting columns that are going to be added to the output table
def get_columns_list(query_manager, model_list, MAKE_ALL_PREDS):
    column_list = []
    #Getting the columns from the table passed to the query manager
    for c in query_manager.table.columns :
        column_list.append(c.copy())
                
    #Creating Columns to mark whether a value has been imputed
    for model in model_list :
        if not MAKE_ALL_PREDS :
            new_c_name = model.test_attribute + "_imputed"
            c = Column(new_c_name, Boolean, nullable=True)
            column_list.append(c)
        else :
            c_orig = query_manager.table.c[model.test_attribute]
            new_c_name = model.test_attribute + "_new"
            c = Column(new_c_name, c_orig.type)
            column_list.append(c)
            
            
    if MAKE_ALL_PREDS :
        #Creating column with information about parcel blocks
        c = Column("block_num", Integer, nullable=True)
        column_list.append(c)

    return column_list

#Just for testing at the moment
if not USING_GUI :
    run_test(sys.argv[1])
