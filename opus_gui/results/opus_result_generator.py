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
    from inprocess.configurations.xml_configuration import XMLConfiguration
    from inprocess.travis.opus_core.indicator_framework.representations.computed_indicator import ComputedIndicator
    from inprocess.travis.opus_core.indicator_framework.maker.maker import Maker
    from opus_gui.results.indicator_framework_interface import IndicatorFrameworkInterface

except ImportError:
    WithOpus = False
    print "Unable to import opus core libs"

class OpusGuiThread(QThread):

    def __init__(self, parentThread, parent, thread_object):
        #parent is a GenerateResultsForm
        QThread.__init__(self, parentThread)
        self.parent = parent
        self.thread_object = thread_object
        
    def run(self):
        #parent.element is an OpusResultGenerator
        self.thread_object.progressCallback = self.progressCallback
        self.thread_object.finishedCallback = self.finishedCallback
        self.thread_object.errorCallback = self.errorCallback
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

class OpusResultVisualizer(object):
    pass

class OpusResultGenerator(object):
    
    def __init__(self, xml_path, domDocument):
        self.xml_path = xml_path
        self.finishedCallback = None
        self.errorCallback = None
        self.guiElement = None
        self.config = None
        self.firstRead = True
        self.domDocument = domDocument
    
    def set_data(self,
                 source_data_name,
                 indicator_name,
                 dataset_name):
        self.source_data_name = source_data_name
        self.indicator_name = indicator_name
        self.dataset_name = dataset_name
        
    def run(self):
        
        if WithOpus:
            succeeded = False
            try:
                # find the directory containing the eugene xml configurations
                fileNameInfo = QFileInfo(self.xml_path)
                fileNameAbsolute = fileNameInfo.absoluteFilePath().trimmed()
                print fileNameAbsolute
                self.config = XMLConfiguration(str(fileNameAbsolute)).get_run_configuration('Eugene_baseline')

                self._generate_results()
                
                succeeded = True
            except:
                succeeded = False
                errorInfo = self.formatExceptionInfo()
                errorString = "Unexpected Error From Model :: " + str(errorInfo)
                print errorInfo
                self.errorCallback(errorString)

            self.finishedCallback(succeeded)
        else:
            pass

    def _generate_results(self):
        
        #TODO eliminate hardcoded package_order
        cache_directory = self.config['cache_directory']
        interface = IndicatorFrameworkInterface(domDocument = self.domDocument)
        
        source_data = interface.get_source_data_from_XML(
                                     source_data_name = self.source_data_name, 
                                     cache_directory = cache_directory)
        indicator = interface.get_indicator_from_XML(
                                     indicator_name = self.indicator_name,
                                     dataset_name = self.dataset_name)
        
        maker = Maker()

        computed_indicator = maker.create(indicator = indicator, 
                                          source_data = source_data)
        
        #TODO: add result to results tree
        
    def _get_current_log(self, key):
        newKey = key
        if WithOpus:
            # We attempt to keep up on the current progress of the model run.  We pass into this
            # function an intial "key" value of 0 and expect to get back a new "key" after the
            # function returns.  It is up to us in this function to use this key to determine
            # what has happened since last time this function was called.
            # In this example we use the key to indicate where in a logfile we last stopped reading
            # and seek into that file point and read to the end of the file and append to the
            # log text edit field in the GUI.
            if self.config is not None and 'cache_directory' in self.config:
                try:
                    log_file = os.path.join(self.config['cache_directory'],
                                          'indicators',
                                          'indicators.log')
                    
                    f = open(log_file)
                    f.seek(key)
                    lines = f.read()
                    newKey = f.tell()
                    if newKey != key:
                        self.guiElement.logText.append(lines)
                    f.close()
                except IOError:
                    if self.firstRead == True:
                        self.guiElement.logText.append("No logfile yet")
                        self.firstRead = False
                    else:
                        self.guiElement.logText.insertPlainText(QString("."))
                #self.guiElement.logText.append("ping")
        return newKey
    
    def formatExceptionInfo(self,maxTBlevel=5):
        import traceback
        cla, exc, trbk = sys.exc_info()
        excName = cla.__name__
        try:
            excArgs = exc.__dict__["args"]
        except KeyError:
            excArgs = "<no args>"
        excTb = traceback.format_tb(trbk, maxTBlevel)
        return (excName, excArgs, excTb)