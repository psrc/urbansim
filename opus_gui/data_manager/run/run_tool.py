# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE


# PyQt5 includes for python bindings to QT
from PyQt5.QtCore import QThread, pyqtSignal

from opus_gui.util.exception_formatter import formatExceptionInfo
from opus_gui.main.controllers.instance_handlers import get_mainwindow_instance

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
        self.emit(pyqtSignal("toolStarting()"))

    def progressCallback(self,percent):
        #print "Ping From Tool"
        self.emit(pyqtSignal("toolProgressPing(PyQt_PyObject)"),percent)

    def logCallback(self,log):
        self.emit(pyqtSignal("toolLogPing(PyQt_PyObject)"),log)

    def finishedCallback(self,success):
        #if success:
        #    print "Success returned from Model"
        #else:
        #    print "Error returned from Model"
        self.emit(pyqtSignal("toolFinished(PyQt_PyObject)"),success)


class OpusTool(object):
    def __init__(self, toolInclude, toolVars={}):
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
            exec(importString, globals())
            self.params = self.buildparams()
            if self.startingCallback != None:
                self.startingCallback()
            success = opusRun(self.progressCallback,self.logCallback,self.toolVars) #@UndefinedVariable
            if self.finishedCallback != None:
                self.progressCallback(100)
                self.finishedCallback(success)
        except ImportError as e:
            print("ImportError: %s" % formatExceptionInfo())
            success = False
            self.logCallback("Error importing %s: %s" % (self.toolInclude, formatExceptionInfo()) )
            self.finishedCallback(success)
        except:
            success = False
            errorInfo = formatExceptionInfo(custom_message = 'Unexpected Error From Tool',plainText=True)
            #self.logCallback("Unexpected Error From Tool %s" % (self.toolInclude))
            self.logCallback(errorInfo)
            self.finishedCallback(success)

