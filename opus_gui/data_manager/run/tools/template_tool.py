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
    
