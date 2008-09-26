# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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


from opus_gui.results_manager.run.indicator_framework.maker.source_data import SourceData
from opus_gui.results_manager.run.indicator_framework.representations.indicator import Indicator
from opus_gui.results_manager.run.indicator_framework.representations.computed_indicator import ComputedIndicator

from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration    
from opus_gui.results_manager.xml_helper_methods import ResultsManagerXMLHelper
from opus_core.database_management.configurations.services_database_configuration import ServicesDatabaseConfiguration
from opus_core.services.run_server.run_manager import RunManager

from sqlalchemy.sql import select

class IndicatorFrameworkInterface:
    def __init__(self, toolboxBase):
        self.toolboxBase = toolboxBase
        self.xml_helper = ResultsManagerXMLHelper(toolboxBase = toolboxBase)
        self.run_manager = RunManager(ServicesDatabaseConfiguration())
        
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
                
    def get_source_data(self, source_data_name, years): 
        source_data_name = str(source_data_name)   
        dataset_pool_configuration = self._get_dataset_pool_configuration()
        run_tbl = self.run_manager.services_db.get_table('run_activity')
        
        if 'cache_directory' in run_tbl.c:
            
            s = select([run_tbl.c.run_id, run_tbl.c.cache_directory],
                       whereclause=run_tbl.c.run_name == source_data_name)
            
            run_id, cache_directory = self.run_manager.services_db.execute(s).fetchone()
        else:
            s = select([run_tbl.c.run_id],
                       whereclause=run_tbl.c.run_name == source_data_name)            
            run_id = self.run_manager.services_db.execute(s).fetchone()[0]
            cache_directory = self.run_manager.get_cache_directory(run_id = run_id)
            
        source_data = SourceData(
                 dataset_pool_configuration = dataset_pool_configuration,
                 run_id = run_id,
                 cache_directory = cache_directory, 
                 name = source_data_name,
                 years = years)
        
        return source_data
        
    def get_indicator(self, indicator_name, dataset_name, indicator_definition = None):

        if indicator_definition is None:
            indicators = self.xml_helper.get_available_indicator_names(
                       attributes = ['dataset', 'source'],
                       return_all = True)
            expression = None
            for indicator in indicators:
                if dataset_name != indicator['dataset'] or \
                    indicator['name'] != indicator_name:
                    continue
                expression = indicator['value']
                attribute = str(expression)
                source = indicator['source']
                break
            
            if expression is None:
                raise Exception('Could not find an indicator %s for dataset %s'%(indicator_name, dataset_name))
        
        else:
            attribute, source = indicator_definition
            
        
        if attribute.find('=') == -1 and source == 'expression':
            attribute = str(indicator_name) + '='+ attribute
        
        new_indicator = Indicator(name = indicator_name,
                                  dataset_name = dataset_name,
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
