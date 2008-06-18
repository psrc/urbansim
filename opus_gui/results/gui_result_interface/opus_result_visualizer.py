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
    from opus_gui.results.indicator_framework.visualizer.visualization_factory import VisualizationFactory
    from opus_gui.results.gui_result_interface.indicator_framework_interface import IndicatorFrameworkInterface
    from opus_gui.results.indicator_framework.visualizer.visualizers.table import Table
    from opus_core.storage_factory import StorageFactory
    from opus_gui.results.gui_result_interface.opus_gui_thread import formatExceptionInfo

except ImportError:
    WithOpus = False
    print "Unable to import opus core libs for opus result visualizer"
    
class OpusResultVisualizer(object):
    def __init__(self, 
                 toolboxStuff, 
                 indicator_type,
                 indicators, 
                 kwargs = None):
        self.finishedCallback = None
        self.errorCallback = None
        self.guiElement = None
        self.config = None
        self.firstRead = True
        self.toolboxStuff = toolboxStuff
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
        interface = IndicatorFrameworkInterface(toolboxStuff = self.toolboxStuff)
        
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
                source_data = interface.get_source_data(
                                             source_data_name = source_data_name, 
                                             years = list(years))
                source_data_objs[source_data_name] = source_data
            else:
                source_data = source_data_objs[source_data_name]
    
            indicator = interface.get_indicator(
                                         indicator_name = indicator_name,
                                         dataset_name = dataset_name)
            
            computed_indicator = interface.get_computed_indicator(indicator = indicator, 
                                                                  source_data = source_data, 
                                                                  dataset_name = dataset_name)
            #####################
            #hack to get plausible primary keys...
            cache_directory = source_data.cache_directory
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