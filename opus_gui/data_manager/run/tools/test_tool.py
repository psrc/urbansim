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
    return 'This is a tool provided strictly for testing purposes.'

