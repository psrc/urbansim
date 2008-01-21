# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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


# PyQt4 includes for python bindings to QT
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os, shutil, sys, tempfile, time

class RunScriptThread(QThread):
    def __init__(self, parent,opusScript):
        QThread.__init__(self, parent)
        self.parent = parent
        self.opusScript = opusScript
        
    def run(self):
        self.opusScript.progressCallback = self.progressCallback
        self.opusScript.logCallback = self.logCallback
        self.opusScript.finishedCallback = self.finishedCallback
        self.opusScript.run()
    
    def StartingCallback(self):
        self.emit(SIGNAL("scriptStarting()"))

    def progressCallback(self,percent):
        #print "Ping From Script"
        self.emit(SIGNAL("scriptProgressPing(PyQt_PyObject)"),percent)

    def logCallback(self,log):
        self.emit(SIGNAL("scriptLogPing(PyQt_PyObject)"),log)

    def finishedCallback(self,success):
        #if success:
        #    print "Success returned from Model"
        #else:
        #    print "Error returned from Model"
        self.emit(SIGNAL("scriptFinished(PyQt_PyObject)"),success)
            

class OpusScript(object):
    def __init__(self,parent,scriptInclude):
        self.parent = parent
        self.scriptInclude = scriptInclude
        self.startingCallback = None
        self.progressCallback = None
        self.logCallback = None
        self.finishedCallback = None

    def buildparams(self):
        return {'param1':'val1','param2':'val2'}
    
    def run(self):
        # Call the script, passing in the callbacks
        #
        # There are really two ways to call the script
        # 1) Call the script as a system command
        # 2) Call the run() function of the script
        #
        # The first option has the benifit of the standard __main__ syntax,
        # but the second option allows for use of the callbacks.
        #
        # The prefered method for opus scripts is the second option
        #
        # EXAMPLE
        #
        try:
            importString = "from %s import opusRun" % (self.scriptInclude)
            print importString
            exec(importString)
            self.params = self.buildparams()
            if self.startingCallback != None:
                self.startingCallback()
            success = opusRun(self.progressCallback,self.logCallback,
                              self.params)
            if self.finishedCallback != None:
                self.finishedCallback(success)
        except ImportError:
            print "Error importing ",self.scriptInclude
            return
        
