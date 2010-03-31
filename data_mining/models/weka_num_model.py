import os
import tempfile
import numpy
import math
import random
import time

from weka_utilities import test_file_creation, feature_selection, Test_result
from data_mining.PrintOutput import PrintOutput

#loads system variables                                                                                  
path = os.environ.get('OPUS_HOME')
path = os.path.join(path, "src", "data_mining", "SYSTEM_VARIABLES.py")
execfile(path) 

class Num_model :

    def __init__(self, xml_elem, MAKE_ALL_PREDS, logCB = None, progressCB = None) :

        #For reporting results
        self.printOut = PrintOutput(logCB, progressCB, PROFILING) 

        #Test specific information
        self.test_attribute = xml_elem.attributes["test_attribute"].value
        
        self.test_classifier = "weka.classifiers.lazy.IBk"
        if xml_elem.hasAttribute("test_classifier") :
            self.test_classifier = xml_elem.attributes["classifier"].value

        self.test_options = "-I -K 20 -X -A weka.core.neighboursearch.KDTree"
        if xml_elem.hasAttribute("options") :
            self.test_options = xml_elem.attributes["options"].value

        #Feature selection information
        self.use_feature_selection = False
        self.using_pca = False
        self.search_class = ""
        self.evaluation_class = ""
        if xml_elem.hasAttribute('fs_evaluation_class'):
            self.use_feature_selection = True

            self.search_class = xml_elem.attributes["fs_search_class"].value
            self.evaluation_class = xml_elem.attributes["fs_evaluation_class"].value
            
            #Checking for pca
            if self.evaluation_class.find("PrincipalComponents") > -1 :
                self.using_pca = True
                
            #Attributes that the search class starts with (Not used with PCA)
            self.start_attributes = []
            if xml_elem.hasAttribute('fs_start_attributes') :
                self.start_attributes = util_get_attribute_list(xml_elem.attributes['fs_start_attributes'].value)  
            
        #Attributes that are used to make the prediction        
        attributes_string = xml_elem.attributes["train_attributes"].value
        self.attributes = util_get_attribute_list(attributes_string)

        #Values that are considered null for the target attribute
        self.null_value_list = []
        elements = xml_elem.getElementsByTagName('null_values')
        if len(elements) > 0 :
            null_val_element = elements[0]
            for element in null_val_element.getElementsByTagName('v') :
    
                attribute = element.attributes['attribute'].value
                type = element.attributes['type'].value
                value = element.attributes['value'].value
                vt = element.attributes['vt'].value
    
                null_dict = {"attribute" : attribute, "type" : type}
    
                if vt == "int" :
                    null_dict["value"] = int(value)
                elif vt == "string" :
                    null_dict["value"] = str(value)
            
                self.null_value_list.append(null_dict)

        #Simply defined null values
        if xml_elem.hasAttribute("null_value") :
            null_value = xml_elem.attributes["null_value"].value
            null_dict = {"attribute" : self.test_attribute, "type" : "E", "value" : int(null_value)}
            self.null_value_list.append(null_dict)

        #Random information
        self.test_type = "Num"
        self.MAKE_ALL_PREDS = MAKE_ALL_PREDS           
        
    def get_predictions(self, query_manager) :

        #Filenames
        test_filename = "test" + str(int(time.time())) + ".arff"
        train_filename = "train" + str(int(time.time())) + ".arff"
        train_log = "train_log" + str(int(time.time())) + ".arff"
        result_filename = "results" + str(int(time.time())) + ".txt"


        #Creates (or clears) files that are used by the binary 
        IS_NUM_TEST = True
        file_creation_info = test_file_creation(IS_NUM_TEST, self.using_pca, test_filename, train_filename, query_manager, self)
        target_values = file_creation_info["target_values"]
        target_value_null = file_creation_info["target_value_null"]
        attribute_indexes = file_creation_info["attribute_indexes"]

        #If there are no null values in the test set
        #And the run is only replacing null values then terminate if no null values
        if not self.MAKE_ALL_PREDS and target_value_null.count(True) == 0 :
            os.remove(test_filename)
            os.remove(train_filename)            
            return None


        #Running feature selection process if needed
        acc_est = {}
        if self.use_feature_selection :
            (test_filename, train_filename, selected_attributes) = feature_selection(test_filename, train_filename, query_manager, file_creation_info, self, IS_NUM_TEST)
            acc_est["selected attributes"] = selected_attributes
                      
        #Running tests
        model_name = "saved_model" + str(int(time.time()))
        path_spef_weka = os.path.join( path, "models", "weka.jar")
        train_string = "java -Xmx1024m -cp " + path_spef_weka + " " + self.test_classifier + " -d " + model_name  + " " + self.test_options + " -t " + train_filename + " >> " + train_log
        test_string = "java -Xmx1024m -cp " +  path_spef_weka + " " + self.test_classifier + " -l " + model_name + " -T " + test_filename + " -p 0 >> " + result_filename

        self.printOut.pLog( "PRED- Training model")
        os.system(train_string)
        self.printOut.pLog( "PRED- Making predictions")
        os.system(test_string)
                    
        #Gathering results for each test instance
        self.printOut.pLog( "PRED- Getting results")
        f = open(result_filename)
        
        prediction_list = []
        confidence_list = []
        
        #For stat keeping
        absolute_diff_list = [] 
        relative_diff_list = []
        
        index = 0
        collect_results = False
        for line in f.readlines() :
            line_list = line.split()
            
            #Getting results
            if collect_results and len(line_list) > 1:
                prediction = float(line_list[2])
                prediction_list.append(prediction)
                confidence_list.append(0.0)
                
                #Getting difference between predicted and actuall results 
                #For non null values
                if not target_value_null[index] :
                    actual = float(target_values[index])
                    diff = math.fabs(actual - prediction)
                    
                    absolute_diff_list.append(diff)
                    if actual > 0 :
                        relative_diff_list.append(diff / actual)
                    else :
                        relative_diff_list.append(-1)
                index += 1
            
            #Seeing if you are at the results portion of the file
            if line.find("inst#") > -1 :
                collect_results = True            
        
        f.close()

        #Gathering accuracy estimations
        f = open(train_log)

        cross_val_info = False
        get_k_value = False
        for line in f.readlines() :
        
            #Getting all performance related metrics
            if cross_val_info :
                line = line.rstrip('\n')
                line = line.rstrip('\t')
                line = line.rstrip('\b')
                line = line.rstrip(' %')
        
                list = line.split('  ')
                if len(list) > 1:
                    attribute = list[0]
                    value = list[len(list) - 1]
                    value = float(value)
                    acc_est[attribute] = value
        
            #Getting parameter search results
            if get_k_value and line.find('using') > -1:
                list = line.split(' ')
                k = int(list[1])
                acc_est["1 Parameter: k value"] = k
                get_k_value = False
        
            #Finding cross validation info                                                                   
            if line.find('Cross-validation') > -1 :
                cross_val_info = True

            #Finding k value info
            if line.find('IB1 instance-based classifier') > -1 :
                get_k_value = True

        f.close()

        #Adding actual performance statistics
        absolute_diff_array = numpy.array(absolute_diff_list)
        relative_diff_array = numpy.array(relative_diff_list)

        absolute_mean = numpy.mean(absolute_diff_array)
        absolute_std = numpy.std(absolute_diff_array)

        relative_mean = numpy.mean(relative_diff_array)
        relative_std = numpy.std(relative_diff_array)
        
        acc_est["2 On test data: mean absolute diff"] = absolute_mean
        acc_est["2 On test data: std absolute diff"] = absolute_std
        acc_est["2 On test data: mean relative diff"] = relative_mean
        acc_est["2 On test data: std relative diff"] = relative_std
        

        #Add number of test instances to the accuracy estimation
        current_test_num = query_manager.current_test_block.parcel_count
        acc_est["test instance count"] = current_test_num / query_manager.group_max
        acc_est["block number"] = (len(query_manager.used_blocks) - 1)*query_manager.group_max + query_manager.group_count
         
        #Removing files
        os.remove(test_filename)
        os.remove(train_filename)
        os.remove(train_log)
        os.remove(result_filename)
        os.remove(model_name)                  
                    
        return Test_result("Num", self.test_attribute, prediction_list, confidence_list, acc_est)

    

#Gets attributes from a string        
def util_get_attribute_list(string):
    initial_list = string.split(",")
    
    list = []
    for attribute in initial_list :
        new = attribute.rstrip(" ")
        new = new.lstrip(" ")
        list.append(str(new))

    return list
        
