# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from data_mining.outlier_det import run_test
import os, sys, subprocess, time
from xml.dom import minidom

def changeDictionaryIntoXml(params):
    
    impl = minidom.getDOMImplementation()
    newdoc = impl.createDocument(None, "test_info", None)
    
    io_info = newdoc.createElement("io_info")
    model_info = newdoc.createElement("model_info")
    
    for key, value in params.iteritems() :
        if key.startswith("io_") :
            nk = key.replace("io_", "", 1)
            io_info.setAttribute(nk, value)
        elif key.startswith("mi_"):
            nk = key.replace("mi_", "", 1)
            model_info.setAttribute(nk, value)
    
    
    top_element = newdoc.documentElement
    top_element.appendChild(io_info)
    top_element.appendChild(model_info)
    
    print newdoc.toprettyxml()
    return newdoc


def opusRun(progressCB,logCB,params=[]):
    param_dict = {}
    logCB("**** Starting Basic Missing Value Replacement ****\n")
    logCB("Input Params ::\n")
    for key, val in params.iteritems():
        param_dict[str(key)] = str(val)
        logCB("%s - %s\n" % (str(key),str(val)))
    
    xml_doc = changeDictionaryIntoXml(param_dict)
    progressCB(0)
    run_test(xml_doc, logCB, progressCB, False)
    progressCB(100)    

    # return 1 for success
    return 1
    
def opusHelp():
    help = 'This is for simple settings'
    return help
    
