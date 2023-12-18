# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from data_mining.outlier_det import run_test
import os, sys, subprocess, time
from xml.dom import minidom

def opusRun(progressCB,logCB,params=[]):
    param_dict = {}
    logCB("**** Starting Basic Outlier Detection ****\n")
    logCB("**** Loading params from a configuration file ****\n")
    logCB("Input Params ::\n")
    for key, val in params.items():
        param_dict[str(key)] = str(val)
    
    xml_doc = param_dict['path_to_config']
    progressCB(0)
    run_test(xml_doc, logCB, progressCB, True)
    progressCB(100)
    
    # return 1 for success
    return 1
    
def opusHelp():
    help = 'This is for simple settings'
    return help
    