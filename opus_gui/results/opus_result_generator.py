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


class OpusIndicatorGroupProcessor(object):
    def __init__(self, 
                 xml_path, 
                 domDocument,
                 model,
                 kwargs = None):
          
        self.generator = OpusResultGenerator(
           xml_path = xml_path,
           domDocument = domDocument,
           model = model                                            
        )
          
        self.visualizer = OpusResultVisualizer(
           xml_path = xml_path,
           domDocument = domDocument,
           indicator_type = None,
           indicators = None,
           kwargs = kwargs                     
        )
        self.finishedCallback = None
        self.errorCallback = None
            
    def set_data(self,                  
                 indicator_defs, 
                 source_data_name,
                 years):
        
        self.indicator_defs = indicator_defs
        self.years = years
        self.source_data_name = source_data_name        
        
    def run(self):
        succeeded = False
        
        try:
            self.visualizations = []
            for (visualization_type, dataset_name), indicators in self.indicator_defs.items():
                indicator_results = []
                for indicator_name in indicators:
                    try:
                        self.generator.set_data(self.source_data_name, 
                                                indicator_name, 
                                                dataset_name, 
                                                self.years)
                        self.generator.run()
                        indicator = {'indicator_name':indicator_name,#self.generator.last_added_indicator_result_name,
                                     'dataset_name':dataset_name,
                                     'source_data_name':self.source_data_name,
                                     'years':self.years}
                        indicator_results.append(indicator)
                        
                    except:
                        print 'could not generate indicator %s'%indicator_name
                self.visualizer.indicator_type = visualization_type
                self.visualizer.indicators = indicator_results
                try:
                    import pydevd;pydevd.settrace()
                except:
                    pass
                self.visualizer.run()
                self.visualizations.append((visualization_type, self.visualizer.get_visualizations()))
            
            succeeded = True
        except:
            succeeded = False
            errorInfo = formatExceptionInfo()
            errorString = "Unexpected Error From Model :: " + str(errorInfo)
            print errorInfo
            self.errorCallback(errorString)

        self.finishedCallback(succeeded)
    
    def get_visualizations(self): 
        return self.visualizations
    
class OpusResultVisualizer(object):
    def __init__(self, 
                 xml_path, 
                 domDocument, 
                 indicator_type,
                 indicators, 
                 kwargs = None):
        self.xml_path = xml_path
        self.finishedCallback = None
        self.errorCallback = None
        self.guiElement = None
        self.config = None
        self.firstRead = True
        self.domDocument = domDocument  
        self.indicator_type = indicator_type
        self.indicators = indicators
        self.visualizations = []
        
        if kwargs == None: kwargs = {}
        self.kwargs = kwargs
        
    def run(self):
        if WithOpus:
            succeeded = False
            try:
                # find the directory containing the eugene xml configurations
                self._visualize()
                succeeded = True
            except:
                succeeded = False
                errorInfo = formatExceptionInfo()
                errorString = "Unexpected Error From Model :: " + str(errorInfo)
                print errorInfo
                if self.errorCallback is not None:
                    self.errorCallback(errorString)
            if self.finishedCallback is not None:
                self.finishedCallback(succeeded)
        else:
            pass
    

        
    def _visualize(self):
        indicators_to_visualize = {}
        interface = IndicatorFrameworkInterface(domDocument = self.domDocument)
        
        #get common years
        years = set([])
        for indicator in self.indicators:
            years |= set(indicator['years'])
            
        source_data_objs = {}
        for indicator in self.indicators:
            indicator_name = indicator['indicator_name']
            source_data_name = indicator['source_data_name']
            dataset_name = indicator['dataset_name']
            
            if source_data_name not in source_data_objs:                
                source_data = interface.get_source_data_from_XML(
                                             source_data_name = source_data_name, 
                                             years = list(years))
                source_data_objs[source_data_name] = source_data
            else:
                source_data = source_data_objs[source_data_name]
    
            indicator = interface.get_indicator_from_XML(
                                         indicator_name = indicator_name,
                                         dataset_name = dataset_name)
            
            computed_indicator = interface.get_computed_indicator(indicator = indicator, 
                                                                  source_data = source_data, 
                                                                  dataset_name = dataset_name)
            #####################
            #hack to get plausible primary keys...
            cache_directory = interface._get_cache_directory(source_data_name)
            _storage_location = os.path.join(cache_directory,
                                             'indicators',
                                             '_stored_data',
                                             repr(source_data.years[0]))
            
            storage = StorageFactory().get_storage(
                           type = 'flt_storage',
                           storage_location = _storage_location)
            cols = storage.get_column_names(
                        table_name = dataset_name)
            ##################
            
            primary_keys = [col for col in cols if col.find('id') != -1]
            computed_indicator.primary_keys = primary_keys
            
            name = computed_indicator.get_file_name(
                suppress_extension_addition = True)
        
            indicators_to_visualize[name] = computed_indicator
            
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
        
        try:
            import pydevd;pydevd.settrace()
        except:
            pass
        
        viz_factory = VisualizationFactory()        
        self.visualizations = viz_factory.visualize(
                                  indicators_to_visualize = indicators_to_visualize.keys(), 
                                  computed_indicators = indicators_to_visualize, 
                                  visualization_type = viz_type, **args)
    
    def get_visualizations(self):
        return self.visualizations

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
                                    value = '',
                                    temporary = True)
        source_data_node = model.create_node(document = document, 
                                    name = 'source_data', 
                                    type = 'string', 
                                    value = self.source_data_name,
                                    temporary = True)
        indicator_node = model.create_node(document = document, 
                                    name = 'indicator_name', 
                                    type = 'string', 
                                    value = self.indicator_name,
                                    temporary = True)        
        dataset_node = model.create_node(document = document, 
                                    name = 'dataset_name', 
                                    type = 'string', 
                                    value = self.dataset_name,
                                    temporary = True)
        year_node = model.create_node(document = document, 
                                    name = 'available_years', 
                                    type = 'string', 
                                    value = ', '.join([repr(year) for year in self.years]),
                                    temporary = True)
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
