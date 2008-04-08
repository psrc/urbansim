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


from opus_gui.results.indicator_framework.representations.visualization import Visualization
from opus_gui.results.indicator_framework.visualizer.visualization_factory import VisualizationFactory
from opus_gui.results.indicator_framework.maker.source_data import SourceData
from opus_gui.results.indicator_framework.representations.indicator import Indicator
from opus_gui.results.indicator_framework.representations.computed_indicator import ComputedIndicator

from opus_gui.results.xml_helper_methods import get_child_values
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration    

from PyQt4.QtCore import QString

class IndicatorFrameworkInterface:
    def __init__(self, domDocument):
        self.domDocument = domDocument
    
    def _get_dataset_pool_configuration(self):
        dataset_pool_config_node = self.domDocument.elementsByTagName(QString('dataset_pool_configuration')).item(0)
        dataset_pool_config_options = get_child_values(parent = dataset_pool_config_node, 
                                                       child_names = ['package_order'])
        
        package_order = [p.strip()[1:-1] 
                         for p in str(dataset_pool_config_options['package_order'])[1:-1].split(',')]
        dataset_pool_configuration = DatasetPoolConfiguration(
             package_order= package_order,
             package_order_exceptions={},
             )

        return dataset_pool_configuration

    def _get_scenario_name(self, source_data_name):
        source_data_node = self.domDocument.elementsByTagName(source_data_name).item(0)
        scenario_name = get_child_values(parent = source_data_node, 
                                 child_names = ['scenario_name'])
        return scenario_name['scenario_name']

    def _get_cache_directory(self, source_data_name):
        source_data_node = self.domDocument.elementsByTagName(QString(source_data_name)).item(0)
        source_data_params = get_child_values(parent = source_data_node, 
                                                       child_names = ['cache_directory'])
        return str(source_data_params['cache_directory'])
                
    def get_source_data_from_XML(self, source_data_name, years):    
        dataset_pool_configuration = self._get_dataset_pool_configuration()
        cache_directory = self._get_cache_directory(source_data_name)
                          
        source_data = SourceData(
                 dataset_pool_configuration = dataset_pool_configuration,
                 cache_directory = cache_directory, 
                 name = '',
                 years = years)
        
        return source_data
        
    def get_indicator_from_XML(self, indicator_name, dataset_name):
        indicator_node = self.domDocument.elementsByTagName(indicator_name).item(0)
        attribute = str(get_child_values(
                           parent = indicator_node,
                           child_names = ['expression'])['expression'])
                
        attribute = attribute.replace('DATASET', dataset_name)
        indicator = Indicator(dataset_name = dataset_name,
                              attribute = attribute)
    
        return indicator
    
    def get_computed_indicator(self, indicator, source_data, dataset_name):
        #TODO: need mapping in XML from dataset to primary keys

        indicator = ComputedIndicator(
                         indicator = indicator, 
                         source_data = source_data, 
                         dataset_name = dataset_name,
                         primary_keys = [])         
        return indicator