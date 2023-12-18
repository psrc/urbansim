#Way of testing the function that will be part of the GUI
from xml.dom import minidom

#Setup env variables
import sys
import os
sys.path.append('/Users/samclark/Desktop/UrbSimSandbox/trunk/urbansim')
sys.path.append('/Users/samclark/Desktop/UrbSimSandbox/trunk/opus_core')
sys.path.append('/Users/samclark/Desktop/UrbSimSandbox/trunk')
os.environ['OPUS_HOME'] = '/Users/samclark/Desktop/UrbSimSandbox'

print("VARIABLES SET")
from .null_val_rep import run_test
import data_mining.PrintOutput

def opusRun(progressCB, logCB, params=[]):
    
    #Stuff for the UrbanSim GUI
    params["_pCB"] = progressCB
    params["_lCB"] = logCB

    xml_doc = changeDictionaryIntoXml(params)
    
    run_test(xml_doc, logCB, progressCB, False)
    
def logCB(line):
    print(line)

def progressCB(x):
    print("Percentage: ", x) 
    
def changeDictionaryIntoXml(params):
    
    impl = minidom.getDOMImplementation()
    newdoc = impl.createDocument(None, "test_info", None)
    
    io_info = newdoc.createElement("io_info")
    model_info = newdoc.createElement("model_info")
    
    for key, value in params.items() :
        if key.startswith("io_") :
            nk = key.replace("io_", "", 1)
            io_info.setAttribute(nk, value)
        elif key.startswith("mi_"):
            nk = key.replace("mi_", "", 1)
            model_info.setAttribute(nk, value)
    
    
    top_element = newdoc.documentElement
    top_element.appendChild(io_info)
    top_element.appendChild(model_info)
    
    print(newdoc.toprettyxml())
    return newdoc


#Info that will be passed to this function
params = {
        "io_input_table_name" : "z_check1",
        "io_input_db_url" : "mysql://root:Schul3r09@localhost/detroit_data",         
        "io_x_column" : 'centroidx',
        "io_y_column" : 'centroidy',        
        "io_id_column" : 'BLDG_ID',
        "io_output_table_name" : "z_sanity_check",
        "io_output_db_url" : "mysql://root:Schul3r09@localhost/UrbanSim", 
        "io_overwrite_table" : "TRUE",
                        
        "mi_type" : "Num",         
        "mi_test_attribute" : "SQFT_PER_UNIT", 
        "mi_null_value" : "0",
        "mi_train_attributes" : "STORIES, centroidx, centroidy"        
}

opusRun(progressCB, logCB, params)
