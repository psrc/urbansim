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
    from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration    

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

def _get_dataset_pool_configuration(domDocument):
    dataset_pool_config_node = domDocument.elementsByTagName(QString('dataset_pool_configuration')).item(0)
    dataset_pool_config_options = get_child_values(parent = dataset_pool_config_node, 
                                                   child_names = ['package_order'])
    
    package_order = str(dataset_pool_config_options['package_order'])[1:-1].split(',')
    dataset_pool_configuration = DatasetPoolConfiguration(
         package_order= package_order,
         package_order_exceptions={},
         )

    return dataset_pool_configuration

class OpusResultVisualizer(object):
    def __init__(self, 
                 xml_path, 
                 domDocument, 
                 indicator_type,
                 source_data_name,
                 indicator_name,
                 dataset_name,
                 years,
                 kwargs = None):
        self.xml_path = xml_path
        self.finishedCallback = None
        self.errorCallback = None
        self.guiElement = None
        self.config = None
        self.firstRead = True
        self.domDocument = domDocument  
        self.indicator_type = indicator_type
        self.source_data_name = source_data_name
        self.indicator_name = indicator_name
        self.dataset_name = dataset_name
        self.years = years     
        self.visualizations = []
        
        if kwargs == None: kwargs = {}
        self.kwargs = kwargs
        
    def run(self):
        if WithOpus:
            succeeded = False
            try:
                # find the directory containing the eugene xml configurations
                fileNameInfo = QFileInfo(self.xml_path)
                fileNameAbsolute = fileNameInfo.absoluteFilePath().trimmed()
                self._visualize(configuration_path = fileNameAbsolute)
                succeeded = True
            except:
                succeeded = False
                errorInfo = formatExceptionInfo()
                errorString = "Unexpected Error From Model :: " + str(errorInfo)
                print errorInfo
                self.errorCallback(errorString)

            self.finishedCallback(succeeded)
        else:
            pass
    

        
    def _visualize(self, configuration_path):
        
        scenario_name = get_scenario_name(domDocument = self.domDocument, 
                                          source_data_name = self.source_data_name)
        self.config = XMLConfiguration(str(configuration_path)).get_run_configuration(scenario_name)

        cache_directory = self.config['cache_directory']

        dataset_pool_configuration = _get_dataset_pool_configuration(self.domDocument)

        interface = IndicatorFrameworkInterface(domDocument = self.domDocument)
        source_data = interface.get_source_data_from_XML(
                                     source_data_name = self.source_data_name, 
                                     cache_directory = cache_directory,
                                     years = self.years,
                                     dataset_pool_configuration = dataset_pool_configuration)
        indicator = interface.get_indicator_from_XML(
                                     indicator_name = self.indicator_name,
                                     dataset_name = self.dataset_name)
        
        computed_indicator = interface.get_computed_indicator(indicator = indicator, 
                                                              source_data = source_data, 
                                                              dataset_name = self.dataset_name)
        #####################
        #hack to get plausible primary keys...
        _storage_location = os.path.join(cache_directory,
                                         'indicators',
                                         '_stored_data',
                                         repr(source_data.years[0]))
        
        storage = StorageFactory().get_storage(
                       type = 'flt_storage',
                       storage_location = _storage_location)
        cols = storage.get_column_names(
                    table_name = self.dataset_name)
        ##################
        
        primary_keys = [col for col in cols if col.find('id') != -1]
        computed_indicator.primary_keys = primary_keys
        print primary_keys

        args = {}
        if self.indicator_type == 'matplotlib_map':
            viz_type = self.indicator_type
        elif self.indicator_type == 'matplotlib_chart':
            viz_type = self.indicator_type
        elif self.indicator_type == 'table_esri':
            viz_type = 'table'
            args['output_type'] = Table.PER_ATTRIBUTE
            args['output_type'] = 'esri'
        elif self.indicator_type == 'table_per_year':
            viz_type = 'table'
            args['output_style'] = Table.PER_YEAR
            args['output_type'] = 'csv'
        elif self.indicator_type == 'table_per_attribute':
            viz_type = 'table'
            args['output_style'] = Table.PER_ATTRIBUTE          
            args['output_type'] = 'csv'
            
        args.update(self.kwargs)
        
        name = computed_indicator.get_file_name(
                                    suppress_extension_addition = True)
        viz_factory = VisualizationFactory()
        
        try:
            import pydevd;pydevd.settrace()
        except:
            pass
        
        self.visualizations = viz_factory.visualize(
                                  indicators_to_visualize = [name], 
                                  computed_indicators = {name:computed_indicator}, 
                                  visualization_type = viz_type, **args)
    
    def get_visualizations(self):
        return self.visualizations

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
                # find the directory containing the eugene xml configurations
                fileNameInfo = QFileInfo(self.xml_path)
                fileNameAbsolute = fileNameInfo.absoluteFilePath().trimmed()
                configuration_path = fileNameAbsolute
                try:
                    import pydevd;pydevd.settrace()
                except:
                    pass
                
                self._generate_results(configuration_path = configuration_path)
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
                self.errorCallback(errorString)

            self.finishedCallback(succeeded)
        else:
            pass

    def _generate_results(self, configuration_path):
        scenario_name = get_scenario_name(domDocument = self.domDocument, 
                                          source_data_name = self.source_data_name)
#        try:
#            import pydevd;pydevd.settrace()
#        except:
#            pass
        self.config = XMLConfiguration(str(configuration_path)).get_run_configuration(scenario_name)
        
        cache_directory = self.config['cache_directory']
        interface = IndicatorFrameworkInterface(domDocument = self.domDocument)
        
        dataset_pool_configuration = _get_dataset_pool_configuration(self.domDocument)
        
        source_data = interface.get_source_data_from_XML(
                                     source_data_name = self.source_data_name, 
                                     cache_directory = cache_directory,
                                     years = self.years,
                                     dataset_pool_configuration = dataset_pool_configuration)
        indicator = interface.get_indicator_from_XML(
                                     indicator_name = self.indicator_name,
                                     dataset_name = self.dataset_name)
        
        maker = Maker()

        computed_indicator = maker.create(indicator = indicator, 
                                          source_data = source_data)
                
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

def get_scenario_name(domDocument, source_data_name):
    source_data_node = domDocument.elementsByTagName(source_data_name).item(0)
    scenario_name = get_child_values(parent = source_data_node, 
                             child_names = ['scenario_name'])
    return scenario_name['scenario_name']
    
    
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