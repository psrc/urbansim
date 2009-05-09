# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE


from opus_gui.results_manager.run.indicator_framework.maker.source_data import SourceData
from opus_gui.results_manager.run.indicator_framework.representations.indicator import Indicator
from opus_gui.results_manager.run.indicator_framework.representations.computed_indicator import ComputedIndicator

from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration

from opus_gui.general_manager.general_manager_functions import get_available_indicator_nodes

class IndicatorFrameworkInterface:
    def __init__(self, project):
        self.project = project

    def _get_dataset_pool_configuration(self):

        # Grab the dataset_pool_configuration from <general>
        package_order_list = self.project.find("general/dataset_pool_configuration/argument[@name='package_order']")
        if package_order_list is None:
            package_order = []
        else:
            package_order_list = package_order_list.text
            package_order = [p.strip()[1:-1] for p in
                             package_order_list[1:-1].split(',')]

        dataset_pool_configuration = DatasetPoolConfiguration(package_order)
        return dataset_pool_configuration

    def get_source_data(self, source_data_name, years):
        run_node = self.project.find('results_manager/simulation_runs/run', name=source_data_name)
        # run_id = run_node.find('run_id').text
        run_id = run_node.get('run_id')
        cache_directory = run_node.find('cache_directory').text

        dataset_pool_configuration = self._get_dataset_pool_configuration()

        source_data = SourceData(
                 dataset_pool_configuration = dataset_pool_configuration,
                 run_id = run_id,
                 cache_directory = cache_directory,
                 name = source_data_name,
                 years = years)

        return source_data

    def get_indicator(self, indicator_name, dataset_name, indicator_definition = None):

        if indicator_definition is not None:
            attribute, source = indicator_definition
        else:
            indicator_nodes = get_available_indicator_nodes(self.project)
            for indicator_node in indicator_nodes:
                if indicator_node.get('name') == indicator_name and \
                    indicator_node.get('dataset') == dataset_name:
                    attribute = (indicator_node.text or '').strip()
                    source = indicator_node.get('source')
                    break
            else:
                raise Exception('Could not find an indicator %s for dataset %s'\
                                 %(indicator_name, dataset_name))

        # Make sure that expressions are prepended by their names
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
