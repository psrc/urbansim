import os
import time

#loads system variables                                                                               
path = os.environ.get('OPUS_HOME')
path = os.path.join(path, "src", "data_mining", "SYSTEM_VARIABLES.py")
execfile(path) 

#utility functions used for WEKA models
def test_file_creation(IS_NUM_TEST, IS_PCA, test_filename, train_filename, query_manager, model):
   
    #Processing information about which rows are null
    query_manager.proc_is_null_list(model)
    
    #Target value lists
    target_values = []
    target_value_null = []
    
    #Get categorical and numeric attributes
    all_cat_atts = query_manager.class_list
    s1 = set(all_cat_atts)
    s2 = set(model.attributes)
    s3 = s1.intersection(s2)
    if not IS_NUM_TEST :
        s3.add(model.test_attribute)
    cat_atts = list(s3)
    
    all_num_atts = query_manager.numeric_list
    s1 = set(all_num_atts)
    s2 = set(model.attributes)
    s3 = s1.intersection(s2)
    num_atts = list(s3)
    
    #First pass is to get possible categorical values
    cat_att_values = {}
    for cat_att in cat_atts :
        cat_att_values[cat_att] = set([])
    
    if not IS_NUM_TEST :
        cat_att_values[model.test_attribute] = set([])
    
    for row in query_manager.current_rows:
        for cat_att in cat_att_values.keys() :
            if row[cat_att] not in cat_att_values[cat_att] :
                cat_att_values[cat_att].add(str(row[cat_att]))
    
    #Getting ID's that insure that the cat atts are one solid string
    cat_id = {}
    for cat_att, values in cat_att_values.iteritems() :
        temp = {}
        id = 0
        for value in values :
            temp[value] = str(id)
            id += 1
        cat_id[cat_att] = temp
    
    #Print to files
    test_f = open(test_filename, "w")
    train_f = open(train_filename, "w")
    
    #Table name
    test_f.write("@relation " + query_manager.table_name + "\n\n")
    train_f.write("@relation " + query_manager.table_name + "\n\n")
    
    #Attribute info
    for cat_att in cat_atts :
        values = cat_att_values[cat_att]
        string = "@attribute " + cat_att + " {"
        for value in values :
            string += cat_id[cat_att][value] + ", "
        string = string.rstrip(", ")
        string +=  "}\n"
        
        test_f.write(string)
        train_f.write(string)
    
    for num_att in num_atts :
        test_f.write("@attribute " + num_att + " real\n")
        train_f.write("@attribute " + num_att + " real\n")
    
    if IS_NUM_TEST and not IS_PCA:
        test_f.write("@attribute " + model.test_attribute + " real\n")
        train_f.write("@attribute " + model.test_attribute + " real\n")
    elif not IS_PCA :
        values = cat_att_values[model.test_attribute]
        string = "@attribute " + model.test_attribute + " {"
        for value in values :
            string += cat_id[model.test_attribute][value] + ", "
        string = string.rstrip(", ")
        string +=  "}\n"
        
        test_f.write(string)
        train_f.write(string)
    
    #Printing data
    test_f.write("\n@data\n")
    train_f.write("\n@data\n")
    
    for index in range(len(query_manager.current_rows)) :
        row = query_manager.current_rows[index]
        
        string = ""
        for cat_att in cat_atts :
            string += cat_id[cat_att][str(row[cat_att])] + ", "
        
        for num_att in num_atts :
            string += str(row[num_att]) + ", "
    
        target_value = str(row[model.test_attribute])
        if not IS_NUM_TEST and not IS_PCA:
            target_value = cat_id[model.test_attribute][target_value]
        elif not IS_PCA and target_value.find("None") > -1 : #Make sure these values can be generated somehow
            target_value = "0"

        if IS_PCA :
            string = string.rstrip(", ")
            string += "\n"
        else :
            string += str(target_value) + "\n"

        #Adding instances that are going to be tested to the list
        if query_manager.is_test_list[index] :
            test_f.write(string)
            target_values.append(target_value)

            if query_manager.is_null_list[index] :
                target_value_null.append(True)
            else :
                target_value_null.append(False)

        #Adding non null instances to the training set
        if not query_manager.is_null_list[index] and query_manager.use_as_training[index]:
            train_f.write(string)
    
    test_f.close()
    train_f.close()

    #Reverse cat_id so that the results can be interpreted
    cat_att_map = {}
    for cat_att, values in cat_id.iteritems() :
        cat_att_map[cat_att] = {}
        for value, id in values.iteritems() :
            cat_att_map[cat_att][id] = value

    #Getting index for each attribute
    attribute_indexes = {}
    index = 1
    for cat_att in cat_atts :
        attribute_indexes[cat_att] = index
        index += 1

    for num_att in num_atts :
        attribute_indexes[num_att] = index
        index += 1

    #Putting all return information in a dictionary
    info = {}
    info["cat_value_id"] = cat_id
    info["cat_att_mapping"] = cat_att_map
    info["target_values"] = target_values
    info["target_value_null"] = target_value_null
    info["attribute_indexes"] = attribute_indexes
    
    return info


def feature_selection(test_filename, train_filename, query_manager, info, model, IS_NUM):
    
    attribute_indexes = info["attribute_indexes"]
    cat_value_id = info["cat_value_id"]
    
    #Code that is executed
    #java -cp weka.jar weka.filters.supervised.attribute.AttributeSelection  \
    #    -E "weka.attributeSelection.CfsSubsetEval" \
    #    -S "weka.attributeSelection.BestFirst -P 6,7" \
    #    -i test_file.arff -o test_file_fs.arff  -r train_file -s train_file_fs

    test_filename_fs = "test_fs" + str(int(time.time())) + ".arff"
    train_filename_fs = "train_fs" + str(int(time.time())) + ".arff"

    path_spef_weka = os.path.join( path, "models", "weka.jar")
            
    fs_string = "java -Xmx1024m -cp " + path_spef_weka + " weka.filters.supervised.attribute.AttributeSelection"
    fs_string += " -E \"" + model.evaluation_class + "\" "
    fs_string += " -S \"" + model.search_class + " -P "
    for attribute in model.start_attributes :
        fs_string += str(attribute_indexes[attribute]) + ","
    fs_string = fs_string.rstrip(",")
    fs_string += "\" -b -i " + test_filename + " -o " + test_filename_fs + " -r " + train_filename + " -s " + train_filename_fs

    #Run filter
    if PROFILING :
        print "FS- Selecting Attributes"
    os.system(fs_string)

    #Change filenames and remove files
    os.remove(test_filename)
    os.remove(train_filename)            
    test_filename = test_filename_fs
    train_filename = train_filename_fs
            
    #For PCA
    if model.using_pca :
        (test_filename, train_filename) = add_target_values(test_filename, train_filename, query_manager, model.test_attribute, cat_value_id, IS_NUM)
            
    #Figure out which attributes were selected
    f = open(test_filename)
    selected_attributes = []
    getting_att_info = True
    while getting_att_info :
        line = f.readline()
                
        if line.find("@attribute") > -1 :
            list = line.split(' ' )
            if list[1] != model.test_attribute :
                selected_attributes.append(list[1])
                
        if line.find("@data") > -1 :
            getting_att_info = False
                    
    f.close()
    
    return (test_filename, train_filename, selected_attributes)


def add_target_values(test_filename, train_filename, query_manager, target_attribute, cat_value_id, IS_NUM) :
    test = test_filename.rstrip(".arff")
    test +=  "_pca.arff"
    train = train_filename.rstrip(".arff")
    train +=  "_pca.arff"
        
    nte = open(test, "w")
    ntr = open(train, "w")
    
    ote = open(test_filename)
    otr = open(train_filename)
    
    #Copy all info header info for both
    getting_header = True
    while getting_header :
        line = ote.readline()
        if line.find("@data") > -1 :
            if IS_NUM :
                nte.write("@attribute " + target_attribute + " real\n")
            else :
                string = "@attribute " + target_attribute + " {"
                for key, value in cat_value_id[target_attribute].iteritems() :
                    string += value + ", "
                string = string.rstrip(", ")
                string +=  "}\n"
                nte.write(string)
                
            getting_header = False
        nte.write(line)
    
    getting_header = True
    while getting_header :
        line = otr.readline()
        if line.find("@data") > -1 :
            if IS_NUM :
                ntr.write("@attribute " + target_attribute + " real\n")
            else :
                string = "@attribute " + target_attribute + " {"
                for key, value in cat_value_id[target_attribute].iteritems() :
                    string += value + ", "
                string = string.rstrip(", ")
                string +=  "}\n"
                ntr.write(string)
                
            getting_header = False
        ntr.write(line)
   
    #Getting first legit lines
    train_line = otr.readline()
    while len(train_line.split(',')) < 2 :
        train_line = otr.readline()
    
    test_line = ote.readline()
    while len(test_line.split(',')) < 2 :
        test_line = ote.readline()

    for index in range(len(query_manager.current_rows)) :
        tv = query_manager.current_rows[index][target_attribute]
        if not IS_NUM :
            tv = cat_value_id[target_attribute][tv]

        #Adding test instances to the test file
        if query_manager.is_test_list[index] :
            test_line = test_line.rstrip('\n')
            test_line += "," + str(tv) + "\n"
            nte.write(test_line)
            test_line = ote.readline() 
        
        #Adding non null instances to the training set
        if not query_manager.is_null_list[index]:
            train_line = train_line.rstrip('\n')
            train_line += "," + str(tv) + "\n"
            ntr.write(train_line)
            train_line = otr.readline() 

    ote.close()
    otr.close()
    os.remove(test_filename)
    os.remove(train_filename)
    
    nte.close()
    ntr.close()
    return (test, train)


#Stores inforation about the results of the test
class Test_result :
    
    def __init__(self, test_type, test_attribute, prediction_list, probability_list, accuracy_est):
        
        #Information about the results of the test
        self.test_attribute = test_attribute
        self.prediction_list = prediction_list
        self.probability_list = probability_list
        self.num_predictions = len(prediction_list)
        self.accuracy_estimation = accuracy_est

        #Random information
        self.test_type = test_type
