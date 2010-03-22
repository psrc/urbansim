#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#
from data_mining.outlier_det import run_test
import os, sys, subprocess, time
from xml.dom import minidom

def opusRun(progressCB,logCB,params=[]):
    param_dict = {}
    logCB("**** Starting Basic Outlier Detection ****\n")
    logCB("**** Loading params from a configuration file ****\n")
    logCB("Input Params ::\n")
    for key, val in params.iteritems():
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
    