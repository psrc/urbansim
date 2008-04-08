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
    
class IndicatorFrameworkInterface:
    def __init__(self, domDocument):
        self.domDocument = domDocument
    
    def get_source_data_from_XML(self, source_data_name, cache_directory, years, dataset_pool_configuration):                        
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