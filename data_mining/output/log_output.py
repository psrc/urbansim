import MySQLdb
from sqlalchemy import *

import os
import shutil
import datetime
import time

#loads system variables                                                                                  
path = os.environ.get('OPUS_HOME')
path = os.path.join(path, "src", "data_mining", "SYSTEM_VARIABLES.py")
execfile(path) 

class Log_manager :
    def __init__(self, xml_elem, config_address):
        
        #Getting info from xml
        self.folder_address = xml_elem.attributes["log_folder_address"].value
        self.config_address = config_address
        
        #Getting info on whether table should be overwritten
        self.overwrite_folder = True
        if xml_elem.hasAttribute("overwrite_folder") and xml_elem.attributes["overwrite_folder"].value == "FALSE" :
            self.overwrite_folder = False
        
        #Checking if table already exists (only removing it if told to)
        if os.path.isdir(self.folder_address) :
            if self.overwrite_folder :
                shutil.rmtree(self.folder_address)
                os.mkdir(self.folder_address)
            else :
                self.folder_address = None
                
        else :
            os.mkdir(self.folder_address)
        
        #Move config into the folder
        self.new_config_address = "Null"
        if self.folder_address != None :
            list = config_address.split(FOLDER_TYPE)
            config_name = list[len(list) - 1]
            config_destination = self.folder_address + FOLDER_TYPE + config_name
            shutil.copy(config_address, config_destination)
        
            self.new_config_address = config_destination
        
        self.block_stats = {}
        
        #Information for the table that keeps track of all test results
        table_name = xml_elem.attributes["overall_results_table_name"].value
        db_url = xml_elem.attributes["overall_results_db_url"].value
        
        #Get SQL connection                                                                    
        db = create_engine(db_url)
        metadata = MetaData(db)
        
        self.table = None
        #If table doesn't exist than create one
        if db.has_table(table_name) :
            self.table = Table(table_name, metadata, autoload=True)
        else :
            self.table = create_table(table_name, metadata)
        
        
    #Collect stats for each attribute
    def get_block_stats(self, query_manager, test_result):
        
        if test_result.test_attribute not in self.block_stats :
            self.block_stats[test_result.test_attribute] = [test_result.accuracy_estimation]
        else :
            self.block_stats[test_result.test_attribute].append(test_result.accuracy_estimation)
    
    #Print a summary of stats for the test
    def store_stats(self, query_manager, output_manager, model_list, start_time, ran_test):
        
        #Aggregate statistics
        path = self.folder_address + FOLDER_TYPE + "overall_stats.txt"
        of = open(path ,"w")
        
        date = datetime.datetime.now()
        
        #Print the overall results
        print "\n\n\n\n"
        print "################# Overall Results ##################"
        print "\n"
        
        #Table and date info
        output_info(of, 'Date: ' + str(date) + '\n')
        output_info(of, 'Input DB: ' + query_manager.db_url + '\n')
        output_info(of, 'Input table: ' + query_manager.table_name + '\n')
        output_info(of, 'Output DB: ' + output_manager.db_url + '\n')
        output_info(of, 'Output table: ' + output_manager.table_name + '\n\n')
                
        #Model and results info
        for model in model_list :
            
            #Checking for models that have actually had tests run (NULL VALUES EXIST)
            if ran_test[model] :
    
                #Print info
                print "\n\n"
                output_info(of, 'Target attribute: ' + model.test_attribute + '\n')
                output_info(of, 'Classifier: ' + model.test_classifier + '\n')
                output_info(of, 'Options: ' + model.test_options + '\n')
                
                #Attributes that were selected by the user
                original_attributes = ""
                for attribute in model.attributes :
                    original_attributes += attribute + ", "
                original_attributes = original_attributes.rstrip(", ")
    
                output_info(of, 'Original Attributes: ' + original_attributes + '\n')
                
                #Attributes that were selected by feature selection
                fs_attribute_counts = {}
                for stat_dict in self.block_stats[model.test_attribute] :
                    if "selected attributes" in stat_dict :
                        for attribute in stat_dict["selected attributes"] :
                            if attribute in fs_attribute_counts :
                                fs_attribute_counts[attribute] += 1 
                            else :
                                fs_attribute_counts[attribute] = 1
                selected_attributes = ""
                for attribute, count in fs_attribute_counts.iteritems() :
                    selected_attributes += str(count) + ":" + attribute + ", "
                selected_attributes = selected_attributes.rstrip(", ")
                output_info(of, 'Selected Attributes: ' + selected_attributes + '\n\n')
                
                #Results
                temp_dict = {}
                for stat_dict in self.block_stats[model.test_attribute] :
                    count = stat_dict["test instance count"]
                    for key, value in stat_dict.iteritems() :
                        if key not in ["test instance count", "Total Number of Instances", "block number", "selected attributes"] :
                            if key not in temp_dict :
                                temp_dict[key] = value*count
                                temp_dict[key + "count"] = count
                            else :
                                temp_dict[key] += value*count
                                temp_dict[key + "count"] += count
                
                output_info(of, 'Statistics for Test:\n')
                keys = temp_dict.keys()
                keys.sort()
                for key in keys :
                    if key not in ["test instance count", "Total Number of Instances", "block number", "selected attributes"] and key.find("count") == -1:
                        value = temp_dict[key]
                        average = float(temp_dict[key]) / temp_dict[key + "count"]
                        average = float("%.3f" % average)
                        output_info(of, '\t' + key + ": " + str(average) + '\n')
                        temp_dict[key] = average
                
                output_info(of, '\n\n\n')
                
                #Print information to overall log table
                info = {}
                info["Date"] = date
                info["DBurl"] = query_manager.db_url
                info["TableName"] = query_manager.table_name
    
                end_time = time.time()
                info["ImputedPerSec"] = query_manager.total_count / (end_time - start_time)
    
                info["TargetAttribute"] = model.test_attribute
                info["OriginalAttributes"] = original_attributes
                
                if model.use_feature_selection :
                    info["FS: Attributes"] = selected_attributes
                    info["FS: Evalulation"] = model.evaluation_class
                    info["FS: Search"] = model.search_class
                else :
                    info["FS: Attributes"] = unicode("")
                    info["FS: Evalulation"] = unicode("")
                    info["FS: Search"] = unicode("")
                
                info["Classifier"] = model.test_classifier
                info["Options"] = model.test_options    
    
                if model.test_type == "Num" :
                    info["ErrorMetric1"] = temp_dict["Root relative squared error"]
                    info["ErrorMetric2"] = temp_dict["Relative absolute error"]
                    info["ErrorMetric3"] = temp_dict["Root mean squared error"]
                    info["ErrorMetric4"] = temp_dict["Mean absolute error"]
                elif model.test_type == "Cat" :
                    info["ErrorMetric1"] = temp_dict["Correctly Classified Instances"]
                    info["ErrorMetric2"] = temp_dict["Kappa statistic"]
                    info["ErrorMetric3"] = -1.0
                    info["ErrorMetric4"] = -1.0
                
                info["ConfigAddress"] = self.new_config_address
                self.table.insert().execute([info])
                        
            
        of.close()
            
        #Per model statistics
        for model in model_list :
            
            #Checking for models that have actually had tests run (NULL VALUES EXIST)
            if ran_test[model] :            
            
                path = self.folder_address + FOLDER_TYPE + model.test_attribute + "_stats.txt"
                f = open(path ,"w")
                
                f.write('Target attribute: ' + model.test_attribute + '\n\n')
                
                #Printing stats for each block
                for stat_dict in self.block_stats[model.test_attribute] :
                    f.write('Block: ' + str(stat_dict["block number"]) + '\n')
                    f.write('Test intance count: ' + str(stat_dict["test instance count"]) + '\n')
                    
                    keys = stat_dict.keys()
                    keys.sort()
                    for key in keys :
                        if key not in ["test instance count", "Total Number of Instances", "block number", "selected attributes"] :
                            value = stat_dict[key]
                            f.write('\t' + key + ": " + str(value) + '\n')
                                
                    f.write('\n')
            
                f.close()
        
        
#Table that keeps track of all results
def create_table(table_name, metadata) :
    
    #Initializing table
    table = Table(table_name, metadata)
    
    #All standard columns
    table.append_column(Column("Date", DateTime, nullable=True))

    table.append_column(Column("TargetAttribute", UnicodeText(200), nullable=True))

    if USE_SCALE :
        table.append_column(Column("ErrorMetric1", Numeric(scale=3), nullable=True))
        table.append_column(Column("ErrorMetric2", Numeric(scale=3), nullable=True))
        table.append_column(Column("ErrorMetric3", Numeric(scale=3), nullable=True))
        table.append_column(Column("ErrorMetric4", Numeric(scale=3), nullable=True))
    else :
        table.append_column(Column("ErrorMetric1", Numeric, nullable=True))
        table.append_column(Column("ErrorMetric2", Numeric, nullable=True))
        table.append_column(Column("ErrorMetric3", Numeric, nullable=True))
        table.append_column(Column("ErrorMetric4", Numeric, nullable=True))
            
    table.append_column(Column("ImputedPerSec", Integer, nullable=True))

    table.append_column(Column("Classifier", UnicodeText(200), nullable=True))
    table.append_column(Column("Options", UnicodeText(200), nullable=True))

    table.append_column(Column("OriginalAttributes", Text, nullable=True))    

    table.append_column(Column("FS: Attributes", Text, nullable=True))
    table.append_column(Column("FS: Evalulation", Text, nullable=True))
    table.append_column(Column("FS: Search", Text, nullable=True))
    
    table.append_column(Column("DBurl", UnicodeText(200), nullable=True))
    table.append_column(Column("TableName", UnicodeText(200), nullable=True))    
    table.append_column(Column("ConfigAddress", Text, nullable=True))
    

            
    #Create table        
    table.create()
    return table

#Util scripts


def output_info(file, string): 
    file.write(string)
    ns = string.rstrip('\n')
    print ns

    
