# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_gui.results_manager.run.opus_result_generator import OpusResultGenerator
from opus_gui.results_manager.run.opus_result_visualizer import OpusResultVisualizer
from opus_gui.util.exception_formatter import formatExceptionInfo
from opus_core.logger import logger

class BatchProcessor(object):
    def __init__(self,
                 project,
                 kwargs = None):

        self.generator = OpusResultGenerator(project)

        self.visualizer = OpusResultVisualizer(
           project = project,
           indicator_type = None,
           indicators = None,
           kwargs = kwargs
        )
        self.finishedCallback = None
        self.errorCallback = None

    def set_data(self,
                visualizations,
                source_data_name,
                years,
                cache_directory = None):

        self.visualization_configurations = visualizations
        self.years = years
        self.source_data_name = source_data_name
        self.cache_directory = cache_directory

    def _get_indicators(self, visualization_config):
        '''
        Extract the indicators from the string (written w/ Python semantics)
        @param visualization_config (dict): a dict representing a batch visualization
        @return: a list of indicators (list(String))
        '''
        indicators_text = visualization_config['indicators']
#        if visualization_type in ['table_per_year']:
        list_str = str(indicators_text)[1:-1]
        indicators = [i.strip()[1:-1] for i in list_str.split(',')]
#        else:
#            indicators = [str(params['indicator'])]

        return indicators

    def _get_viz_args(self, visualization_type, params, indicators):
        args = {}

        if visualization_type == 'tab':
            output_type = str(params['output_type'])
            args['output_type'] = output_type
            if 'name' in params:
                args['name'] = params['name']
            if output_type == 'fixed_field':
                list_str = str(params['fixed_field_specification'])[1:-1]
                spec = [i.strip()[1:-1] for i in list_str.split(',')]
                args['fixed_field_format'] = zip(indicators,spec)
                args['fixed_field_format'].insert(0,('id',str(params['id_format'])))
            elif output_type == 'sql':
                from opus_core.database_management.configurations.indicators_database_configuration import IndicatorsDatabaseConfiguration
                args['storage_location'] = IndicatorsDatabaseConfiguration(database_name = str(params['database_name']))
            elif output_type == 'esri':
                args['storage_location'] = str(params['storage_location'])
            elif output_type == 'tab':
                if 'output_style' in params:
                    args['output_style'] = int(str(params['output_style']))

        elif visualization_type == 'mapnik_map' or visualization_type == 'mapnik_animated_map' :
            try:
                args['mapnik_bucket_labels'] = params['mapnik_bucket_labels']
                args['mapnik_bucket_ranges'] = params['mapnik_bucket_ranges']
                args['mapnik_bucket_colors'] = params['mapnik_bucket_colors']
                args['mapnik_resolution'] = params['mapnik_resolution']
                args['mapnik_page_dims'] = params['mapnik_page_dims']
                args['mapnik_map_lower_left'] = params['mapnik_map_lower_left']
                args['mapnik_map_upper_right'] = params['mapnik_map_upper_right']
                args['mapnik_legend_lower_left'] = params['mapnik_legend_lower_left']
                args['mapnik_legend_upper_right'] = params['mapnik_legend_upper_right']
            except KeyError: 
                # these are the default bucket label, range, and color values
                # these default values are also hard-coded in opus_gui.results_manager.controllers.dialogs.abstract_configure_batch_indicator_visualization.py
                args['mapnik_bucket_labels'] = 'range_labels'
                args['mapnik_bucket_ranges'] = 'linear_scale'
                args['mapnik_bucket_colors'] = '#e0eee0, #c7e9c0, #a1d99b, #7ccd7c, #74c476, #41ab5d, #238b45, #006400, #00441b, #00340b' # green
                args['mapnik_resolution'] = '96'
                args['mapnik_page_dims'] = '8.5,5.5'
                args['mapnik_map_lower_left'] = '0.5,0.5'
                args['mapnik_map_upper_right'] = '6.0,5.0'
                args['mapnik_legend_lower_left'] = '6.5,0.5'
                args['mapnik_legend_upper_right'] = '6.9,5.0'
                
        return args

    def run(self, args = {}):
        succeeded = False

        if self.errorCallback is not None:
            self.generator.errorCallback = self.errorCallback
            self.visualizer.errorCallback = self.errorCallback

#        try:
#            import pydevd;pydevd.settrace()
#        except:
#            pass

        try:
            self.visualizations = []
            
            for (visualization_type, dataset_name, params) in self.visualization_configurations:                
                indicator_results = []
                indicators = self._get_indicators(params)
                for indicator_name in indicators:
                    try:
                        self.generator.set_data(self.source_data_name,
                                                indicator_name,
                                                dataset_name,
                                                self.years,
                                                cache_directory = self.cache_directory)
                        self.generator.run()
                        indicator = {'indicator_name':indicator_name,
                                     'dataset_name':dataset_name,
                                     'source_data_name':self.source_data_name,
                                     'years':self.years}
                        indicator_results.append(indicator)

                    except:
                        logger.log_warning('could not generate indicator %s'%indicator_name)
                self.visualizer.indicator_type = visualization_type
                self.visualizer.indicators = indicator_results

                viz_args = self._get_viz_args(visualization_type, params, indicators)
                self.visualizer.run(args = viz_args, cache_directory = self.cache_directory)
                if self.visualizer.get_visualizations() != []:
                    self.visualizations.append((visualization_type, self.visualizer.get_visualizations()))

            succeeded = True
        except:
            succeeded = False
            errorInfo = formatExceptionInfo(custom_message = 'Unexpected error in the batch processor')
            self.errorCallback(errorInfo)

        if self.finishedCallback: self.finishedCallback(succeeded)

    def get_visualizations(self):
        return self.visualizations
