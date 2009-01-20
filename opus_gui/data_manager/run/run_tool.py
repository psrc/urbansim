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


# PyQt4 includes for python bindings to QT
from PyQt4.QtCore import QThread, SIGNAL

from opus_gui.util.exception_formatter import formatExceptionInfo
from opus_gui.main.controllers.mainwindow import get_mainwindow_instance

class RunToolThread(QThread):
    def __init__(self,opusTool):
        QThread.__init__(self, get_mainwindow_instance())
        self.opusTool = opusTool

    def run(self):
        self.opusTool.startingCallback = self.startingCallback
        self.opusTool.progressCallback = self.progressCallback
        self.opusTool.logCallback = self.logCallback
        self.opusTool.finishedCallback = self.finishedCallback
        #print "Thread Prio Start - %s" % (str(self.priority()))
        #self.setPriority(QThread.LowPriority)
        #print "Thread Prio Set - %s" % (str(self.priority()))
        self.opusTool.run()

    def startingCallback(self):
        self.emit(SIGNAL("toolStarting()"))

    def progressCallback(self,percent):
        #print "Ping From Tool"
        self.emit(SIGNAL("toolProgressPing(PyQt_PyObject)"),percent)

    def logCallback(self,log):
        self.emit(SIGNAL("toolLogPing(PyQt_PyObject)"),log)

    def finishedCallback(self,success):
        #if success:
        #    print "Success returned from Model"
        #else:
        #    print "Error returned from Model"
        self.emit(SIGNAL("toolFinished(PyQt_PyObject)"),success)


class OpusTool(object):
    def __init__(self, toolInclude, toolVars=[]):
        self.toolInclude = toolInclude
        self.toolVars = toolVars
        self.startingCallback = None
        self.progressCallback = None
        self.logCallback = None
        self.finishedCallback = None

    def buildparams(self):
        return {'param1':'val1','param2':'val2'}

    def run(self):
        # Call the tool, passing in the callbacks
        #
        # There are really two ways to call the tool
        # 1) Call the tool as a system command
        # 2) Call the run() function of the tool
        #
        # The first option has the benifit of the standard __main__ syntax,
        # but the second option allows for use of the callbacks.
        #
        # The prefered method for opus tools is the second option
        #
        # EXAMPLE
        #
        try:
            importString = "from %s import opusRun" % (self.toolInclude)
            #print importString
            exec(importString)
            self.params = self.buildparams()
            if self.startingCallback != None:
                self.startingCallback()
            success = opusRun(self.progressCallback,self.logCallback,self.toolVars)
            if self.finishedCallback != None:
                self.progressCallback(100)
                self.finishedCallback(success)
        except ImportError:
            print "Error importing ",self.toolInclude
            success = False
            self.logCallback("Error importing %s" % (self.toolInclude))
            self.finishedCallback(success)
        except:
            success = False
            errorInfo = formatExceptionInfo(custom_message = 'Unexpected Error From Tool',plainText=True)
            #self.logCallback("Unexpected Error From Tool %s" % (self.toolInclude))
            self.logCallback(errorInfo)
            self.finishedCallback(success)

