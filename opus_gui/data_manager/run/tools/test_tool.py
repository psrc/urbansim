# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import time

def opusRun(progressCB, logCB, params=[]):
    param_dict = {}
    logCB("Starting the run method of the diagnostic tool\n")
    logCB("Tool filename: %s\n" % __file__)
    logCB("Listing of input parameters:\n")
    for key, val in params.iteritems():
        param_dict[str(key)] = str(val)
        logCB("%s=%s\n" % (str(key),str(val)))
    
    logCB("Testing progress callback with delay of 2 seconds between steps\n")
    time.sleep(2)
    logCB("Progress test (value = 0)\n")
    progressCB(0)
    time.sleep(2)
    logCB("Progress test midway (value = 50)\n")
    progressCB(50)
    time.sleep(2)
    logCB("Progress test complete (value = 100)\n")
    progressCB(100)
    return 1 # 1 = Success
    
def opusHelp():
    return 'This is a tool provided for testing purposes.'

