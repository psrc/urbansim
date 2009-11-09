# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os, sys, subprocess, time

def opusRun(progressCB,logCB,params=[]):
    param_dict = {}
    logCB("**** Starting Template Tool Execution ****\n")
    logCB("Input Params ::\n")
    for key, val in params.iteritems():
        param_dict[str(key)] = str(val)
        logCB("%s - %s\n" % (str(key),str(val)))
    
    logCB("Starting to execute ::\n")
    # Do a fake loop for testing purposes
    for x in xrange(0,10,1):
        if logCB:
            logCB("Executing Loop - %s\n" % (str(x)))
        if progressCB:
            progressCB(x*10)
        time.sleep(1)

    # return 1 for success
    return 1
    
def opusHelp():
    help = 'This tool will ... (FILL ME IN)'
    return help
    
