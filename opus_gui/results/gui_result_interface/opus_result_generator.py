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
    from opus_gui.results.gui_result_interface.opus_gui_thread import formatExceptionInfo

except ImportError:
    WithOpus = False
    print "Unable to import opus core libs"


class OpusResultGenerator(object):
    
    def __init__(self, xml_path, domDocument, model):
        self.xml_path = xml_path
        self.finishedCallback = None
        self.errorCallback = None
        self.guiElement = None
        self.cache_directory = None
        self.firstRead = True
        self.domDocument = domDocument
        self.model = model
    
    def set_data(self,
                 source_data_name,
                 indicator_name,
                 dataset_name,
                 years):
        self.source_data_name = source_data_name
        self.indicator_name = indicator_name
        self.dataset_name = dataset_name
        self.years = years
        
    def run(self):
        
        if WithOpus:
            succeeded = False
            try:
                try:
                    import pydevd;pydevd.settrace()
                except:
                    pass
                
                self._generate_results()
                succeeded = True
            except Exception, e:
                succeeded = False
                (exception_type, args, trace) = formatExceptionInfo()
                error_characterization = 'Unexpected Error From Model'
                error_message = str(e)
                errorString = '%s :: %s \n%s\n%s%s'%(
                    error_characterization,
                    exception_type,
                    args,
                    ''.join(trace),
                    error_message                                   
                )
                print errorString
                if self.errorCallback is not None:
                    self.errorCallback(errorString)
            if self.finishedCallback is not None:
                self.finishedCallback(succeeded)
        else:
            pass

    def _generate_results(self):
#        try:
#            import pydevd;pydevd.settrace()
#        except:
#            pass
        
        interface = IndicatorFrameworkInterface(domDocument = self.domDocument)
        
        source_data = interface.get_source_data_from_XML(
                                     source_data_name = self.source_data_name, 
                                     years = self.years)
        indicator = interface.get_indicator_from_XML(
                                     indicator_name = self.indicator_name,
                                     dataset_name = self.dataset_name)
        
        maker = Maker()
        self.cache_directory = interface._get_cache_directory(self.source_data_name)

        computed_indicator = maker.create(indicator = indicator, 
                                          source_data = source_data)
        self.update_results_xml()

    def update_results_xml(self):
        print "update results"
        model = self.model
        document = self.domDocument
        
        name = '%s.%s.%s'%(self.indicator_name, 
            self.dataset_name, 
            self.source_data_name)
        
        self.last_added_indicator_result_name = name
        
        newNode = model.create_node(document = document, 
                                    name = name, 
                                    type = 'indicator_result', 
                                    value = '')
        source_data_node = model.create_node(document = document, 
                                    name = 'source_data', 
                                    type = 'string', 
                                    value = self.source_data_name)
        indicator_node = model.create_node(document = document, 
                                    name = 'indicator_name', 
                                    type = 'string', 
                                    value = self.indicator_name)        
        dataset_node = model.create_node(document = document, 
                                    name = 'dataset_name', 
                                    type = 'string', 
                                    value = self.dataset_name)
        year_node = model.create_node(document = document, 
                                    name = 'available_years', 
                                    type = 'string', 
                                    value = ', '.join([repr(year) for year in self.years]))                
        parent = model.index(0,0,QModelIndex()).parent()
        index = model.findElementIndexByName("Results", parent)[0]
        if index.isValid():
            model.insertRow(0,
                            index,
                            newNode)
        else:
            print "No valid node was found..."
        
        child_index = model.findElementIndexByName(name, parent)[0]
        if child_index.isValid():
            for node in [dataset_node, indicator_node, source_data_node, year_node]:
                model.insertRow(0,
                                child_index,
                                node)
        else:
            print "No valid node was found..."
        
        model.emit(SIGNAL("layoutChanged()"))
                
    def _get_current_log(self, key):
        newKey = key
        if WithOpus:
            # We attempt to keep up on the current progress of the model run.  We pass into this
            # function an initial "key" value of 0 and expect to get back a new "key" after the
            # function returns.  It is up to us in this function to use this key to determine
            # what has happened since last time this function was called.
            # In this example we use the key to indicate where in a logfile we last stopped reading
            # and seek into that file point and read to the end of the file and append to the
            # log text edit field in the GUI.
            if self.cache_directory is not None:
                try:
                    log_file = os.path.join(self.cache_directory,
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