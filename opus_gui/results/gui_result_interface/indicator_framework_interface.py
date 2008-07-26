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


from opus_gui.results.indicator_framework.maker.source_data import SourceData
from opus_gui.results.indicator_framework.representations.indicator import Indicator
from opus_gui.results.indicator_framework.representations.computed_indicator import ComputedIndicator

from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration    
from opus_gui.results.xml_helper_methods import ResultsManagerXMLHelper

class IndicatorFrameworkInterface:
    def __init__(self, toolboxStuff):
        self.toolboxStuff = toolboxStuff
        self.xml_helper = ResultsManagerXMLHelper(toolboxStuff = toolboxStuff)
        
    def _get_dataset_pool_configuration(self):
        _, package_order = self.xml_helper.get_element_attributes(
                                   node_name = 'dataset_pool_configuration', 
                                   node_type = 'class', 
                                   child_attributes = ['package_order'])        
        
        package_order = [p.strip()[1:-1] 
                         for p in str(package_order['package_order'])[1:-1].split(',')]

        dataset_pool_configuration = DatasetPoolConfiguration(
             package_order= package_order,
             package_order_exceptions={},
             )

        return dataset_pool_configuration
                
    def get_source_data(self, source_data_name, years, cache_directory = None):    
        dataset_pool_configuration = self._get_dataset_pool_configuration()
        if cache_directory is None:
            _, cache_directory = self.xml_helper.get_element_attributes(
                                    node_name = source_data_name, 
                                    node_type = 'source_data',
                                    child_attributes = ['cache_directory'])
            cache_directory = str(cache_directory['cache_directory'])
                                  
        source_data = SourceData(
                 dataset_pool_configuration = dataset_pool_configuration,
                 cache_directory = cache_directory, 
                 name = '',
                 years = years)
        
        return source_data
        
    def get_indicator(self, indicator_name, dataset_name):

        indicators = self.xml_helper.get_available_indicator_names(
                   attributes = ['dataset'])
        expression = None
        for indicator in indicators:
            if dataset_name != indicator['dataset'] or \
                indicator['name'] != indicator_name:
                continue
            expression = indicator['value']
        
        if expression is None:
            raise Exception('Could not find an indicator %s for dataset %s'%(indicator_name, dataset_name))
        
        attribute = str(expression)
        if attribute.find('=') == -1:
            attribute = str(indicator_name) + '='+ attribute
        
        new_indicator = Indicator(dataset_name = dataset_name,
                              attribute = attribute)
        return new_indicator
    
    def get_computed_indicator(self, indicator, source_data, dataset_name):
        #TODO: need mapping in XML from dataset to primary keys

        indicator = ComputedIndicator(
                         indicator = indicator, 
                         source_data = source_data, 
                         dataset_name = dataset_name,
                         primary_keys = [])         
        return indicator
