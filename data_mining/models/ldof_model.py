import os
import time
import tempfile
import numpy
import math
import random

from data_mining.PrintOutput import PrintOutput

#loads system variables
path = os.environ.get('OPUS_HOME')
execfile(path + "\\src\\data_mining\\" + "SYSTEM_VARIABLES.py") 

#Stores information about the test that was run
class Test_result :
    
    def __init__(self, lof_lists, lof_id_lists):

        #Information about the results of the test
        self.lof_lists = lof_lists
        self.lof_id_lists = lof_id_lists

        #Random information
        self.test_type = "LDOF"

class LDOF_model :

    def __init__(self, xml_elem, logCB = None, progressCB = None) :

        #For reporting results
        self.printOut = PrintOutput(logCB, progressCB, PROFILING) 

        #KNN tuning parameters
        self.k = 10 #Make this 1 more than the number of columns
        self.num_display = 10
        self.num_mod = 1

        #Attributes that are used to make the prediction
        attributes_string = xml_elem.attributes['attributes'].value
        self.attributes = util_get_attribute_list(attributes_string)

        #NOT ACTUALLY USED, JUST MAKES IT SO KNN LIBRARY CAN BE USED
        self.test_attribute = None
        
        #Sets of attributes that must be considered as a whole
        self.attribute_combinations = []
        
        #Set all weights to 1
        self.initialized_weights = {}
        for attribute in self.attributes :
            self.initialized_weights[attribute] = 1

        #Attributes that will get there values log transformed to produce better results
        if xml_elem.hasAttribute('log_trans_attributes') :
            log_trans_string = xml_elem.attributes['log_trans_attributes'].value
            temp_atts_list = util_get_attribute_list(log_trans_string)
            self.log_trans_atts = set(temp_atts_list)

        self.null_value_list = [] #NOT USED

        #Random information
        self.test_type = "LDOF"

                     
    def get_predictions(self, data_profiler) :

        #Creates (or clears) files that are used by the binary 
        self.initialize_files()

        #Put data into files
        self.create_input_files(data_profiler)

        #Create the configuration file
        self.util_create_config(data_profiler)
        
        #Getting list of predictions and confidences
        #(This runs the binary with the config as a input)
        os.system(BINARY + ' ' + self.config_file  + ' >> ' + self.results_file)
        (lof_lists, lof_id_lists) = self.util_get_results(self.results_file)        
                    
        #Removes files used by the binary
        self.remove_files()
                    
        return Test_result(lof_lists, lof_id_lists)

    
    #util function
    #Gets the results from the result file
    #Also removes the files that were being used
    def util_get_results(self, filename) :
        start_time = int(time.time())
        self.printOut.pLog( "LDOF- Getting results" )
        
        f = open(filename)
        predictions = []
        confidences = []
    
        lof_lists = []
        lof_id_lists = []
    
        results_portion = False
        index = 0
        for line in f.readlines() :
            
            #Find better way to identify comments
            if line.find('#') < 0 and results_portion:
                line_list = line.split(', ')
                
                predictions.append(0)
                confidences.append(0)
                
                #Getting lof values for the line
                lof_list = []
                lof_id_list = []
                num_check = (self.k*2) / self.num_mod
                for i in range(num_check + 1) :
                    if i == 0 :
                        id = line_list[i]
                    elif i % 2 == 1 :
                        lof_list.append(1000*float(line_list[i])) #Don't adjust value like this
                    else :
                        lof_id_list.append(int(line_list[i]))
                        
                lof_lists.append(lof_list)
                lof_id_lists.append(lof_id_list)
                
                index += 1

            else :
                stripped = line.rstrip('\n')
                self.printOut.pLog("LDOF- " + stripped)
    
            #Finding the portion of the output file that has results
            if line.find("Printing final results:") > -1 :
                results_portion = True
        
        end_time = int(time.time())
        self.printOut.pLog( "LDOF- Time reading results: " + str( end_time - start_time ))
        
        return [lof_lists, lof_id_lists]
    
    #util function
    #Creates a configuration file that is used by the 
    #binary in order to run the test
    def util_create_config(self, data_profiler) :
           
        #Modifying the list of attribute ids
        #making sure the ones that are connected are represented as such
        #This means they have the same id in the configuration file
        #Also, the weights that are specified are given as well
        weights_list = []
        for index in range(len(data_profiler.attribute_id_list)) :
            id = data_profiler.attribute_id_list[index]
            attribute = data_profiler.attribute_id_dict[id]

            #Setting right IDs
            for combo in self.attribute_combinations :
                if attribute in combo :
                    data_profiler.attribute_id_list[index] = data_profiler.id_attribute_dict[combo[0]]
            
            #Setting right weights
            if attribute in self.initialized_weights :
                weights_list.append(self.initialized_weights[attribute])
            else :
                weights_list.append(0)
           
        #Printing information into the configuration file
        f = open(self.config_file, 'w')
    
        f.write("test_file: " + self.test_filename + "\n")
        f.write("train_file: " + self.train_filename + "\n")
    
        f.write("number_neighbors: " + str(self.k) + "\n")
        f.write("number_display: " + str(self.num_display) + "\n")
        f.write("number_mod: " + str(self.num_mod) + "\n")
    
        f.write("columns_attribute:")
        for i in data_profiler.attribute_id_list :
            f.write(" " + str(i))
        f.write("\n")
        
        f.write("initial_weights:")
        for weight in weights_list :
            f.write(" " + str(weight))
        f.write("\n")
        
        f.close()
    
    #util function
    #Gets information from the data_profiler object to files
    def create_input_files(self, data_profiler):
        start_time = int(time.time())
              
        #Just loading data structures
        test_labels = []
        test_samples = []
        test_ids = []
        
        train_labels = []
        train_samples = []
        train_ids = []
      
        for i in range(len(data_profiler.labels)) :
            #Adding instances that are going to be tested to the list
            if data_profiler.query_manager.is_test_list[i] :
                test_labels.append(data_profiler.labels[i])
                test_samples.append(data_profiler.samples[i])
                test_ids.append(i)
            
            #Adding non null instances to the training set
            if not data_profiler.query_manager.is_null_list[i]:
                train_labels.append(data_profiler.labels[i])
                train_samples.append(data_profiler.samples[i])
                train_ids.append(i)
        
        #Create test and train files
        self.util_create_valid_file_from_samples(test_labels, test_samples, test_ids, self.test_filename)
        self.util_create_valid_file_from_samples(train_labels, train_samples, train_ids, self.train_filename)

        #Isn't used but something needs to be passed to KNN        
        self.util_create_valid_file_from_samples([], [], [], self.val_filename)
        
        #Re-setting transformation information in data profiler
        data_profiler.log_trans_atts = set([])
    
        end_time = int(time.time())
        self.printOut.pLog( "LDOF- Time creating input files: " + str( end_time - start_time ))
    
    #util function
    #Creates files that will be used by the KNN binary                                                                     
    def util_create_valid_file_from_samples(self, labels, samples, id_list, filename) :
        f = open(filename, 'w')
        index = 0
        for sample in samples :
            line = str( labels[index] )
            line += " " + str(id_list[index])
            keys = sample.keys()
            keys.sort()
            for key in keys :
                line += " " + str(key) + ":" + str(sample[key])
            line += "\n"
            f.write(line)
            index += 1
    
        f.close()



    def initialize_files(self):

        #Creating unique file names
        self.test_filename = 'LDOF_TEST_INPUT_FILE' + str(int(time.time())) + '.TXT'
        self.train_filename = 'LDOF_TRAIN_INPUT_FILE' + str(int(time.time())) + '.TXT'
        self.val_filename = 'LDOF_VAL_FILE' + str(int(time.time())) + '.TXT'        
        self.results_file = 'LDOF_RESULTS_FILE' + str(int(time.time())) + '.TXT'
        self.config_file = 'LDOF' + str(int(time.time())) + '.cfg'   
        
        #Initializing files
        os.system('echo \"\" > ' + self.config_file)
        os.system('echo \"\" > ' + self.results_file)
        os.system('echo \"\" > ' + self.test_filename)
        os.system('echo \"\" > ' + self.train_filename)
        os.system('echo \"\" > ' + self.val_filename)

    def remove_files(self):
        os.remove(self.config_file)
        os.remove(self.results_file)
        os.remove(self.test_filename)
        os.remove(self.train_filename) 
        os.remove(self.val_filename)
        
#Gets attributes from a string        
def util_get_attribute_list(string):
    initial_list = string.split(",")
    
    list = []
    for attribute in initial_list :
        new = attribute.rstrip(" ")
        new = new.lstrip(" ")
        list.append(str(new))

    return list        
