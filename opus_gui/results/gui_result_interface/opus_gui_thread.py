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
import os, sys

try:
    WithOpus = True
    #from opus_gui.configurations.xml_configuration import XMLConfiguration
    from opus_core.configurations.xml_configuration import XMLConfiguration
    from opus_gui.results.indicator_framework.representations.computed_indicator import ComputedIndicator
    from opus_gui.results.indicator_framework.maker.maker import Maker
    from opus_gui.results.indicator_framework.visualizer.visualization_factory import VisualizationFactory
    from opus_gui.results.indicator_framework_interface import IndicatorFrameworkInterface
    from opus_gui.results.xml_helper_methods import get_child_values
    from opus_gui.results.indicator_framework.visualizer.visualizers.table import Table
    from opus_core.storage_factory import StorageFactory

except ImportError:
    WithOpus = False
    print "Unable to import opus core libs"

class OpusGuiThread(QThread):

    def __init__(self, parentThread, parent, thread_object):
        #parent is a GenerateResultsForm
        QThread.__init__(self, parentThread)
        self.parent = parent
        self.thread_object = thread_object
        
    def run(self, 
            progressCallback = None,
            finishedCallback = None,
            errorCallback = None):
    
        
        if progressCallback is None:
            progressCallback = self.progressCallback
        if finishedCallback is None:
            finishedCallback = self.finishedCallback
        if errorCallback is None:
            errorCallback = self.errorCallback
            
        self.thread_object.progressCallback = progressCallback
        self.thread_object.finishedCallback = finishedCallback
        self.thread_object.errorCallback = errorCallback
        self.thread_object.run()
        
    def progressCallback(self,percent):
        print "Ping From Model"
        self.emit(SIGNAL("runPing(PyQt_PyObject)"),percent)

    def finishedCallback(self,success):
        if success:
            print "Success returned from Model"
        else:
            print "Error returned from Model"
        self.emit(SIGNAL("runFinished(PyQt_PyObject)"),success)

    def errorCallback(self,errorMessage):
        self.emit(SIGNAL("runError(PyQt_PyObject)"),errorMessage)

    
def formatExceptionInfo(maxTBlevel=5):
    import traceback
    cla, exc, trbk = sys.exc_info()
    excName = cla.__name__
    try:
        excArgs = exc.__dict__["args"]
    except KeyError:
        excArgs = "<no args>"
    excTb = traceback.format_tb(trbk, maxTBlevel)
    return (excName, excArgs, excTb)