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

try:
    WithOpus = True
    from opus_gui.results.gui_result_interface.opus_result_generator import OpusResultGenerator
    from opus_gui.results.gui_result_interface.opus_result_visualizer import OpusResultVisualizer
    from opus_gui.results.gui_result_interface.opus_gui_thread import formatExceptionInfo
except ImportError:
    WithOpus = False
    print "Unable to import opus core libs for opus indicator group processor"

class BatchProcessor(object):
    def __init__(self, 
                 toolboxStuff,
                 kwargs = None):
          
        self.generator = OpusResultGenerator(
           toolboxStuff = toolboxStuff                                            
        )
          
        self.visualizer = OpusResultVisualizer(
           toolboxStuff = toolboxStuff,
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
        
    def _get_indicators(self, visualization_type, params):
        
        if visualization_type in ['table_per_year']:
            list_str = str(params['indicators'])[1:-1]
            indicators = [i.strip()[1:-1] for i in list_str.split(',')]
        else:
            indicators = [str(params['indicator'])]

        return indicators
        
    def _get_viz_args(self, visualization_type, params, indicators):
        args = {}
            
        if visualization_type in ['table_per_year', 'table_per_attribute']:
            output_type = str(params['output_type'])
            args['output_type'] = output_type
            args['name'] = params['name']
            if output_type == 'fixed_field':
                list_str = str(params['fixed_field_specification'])[1:-1]
                spec = [i.strip()[1:-1] for i in list_str.split(',')]
                args['fixed_field_format'] = zip(indicators,spec)
                args['fixed_field_format'].insert(0,('id',str(params['id_format'])))   
            elif output_type == 'sql':
                from opus_core.database_management.database_configuration import DatabaseConfiguration
                args['storage_location'] = DatabaseConfiguration(database_name = str(params['database_name']),
                                                                 test = True)
                
        return args
            
    def run(self, args = {}):
        succeeded = False
        
        try:
            import pydevd;pydevd.settrace()
        except:
            pass
        
        try:
            self.visualizations = []
            for (visualization_type, dataset_name, params) in self.visualization_configurations:
                indicator_results = []
                indicators = self._get_indicators(visualization_type, params)
                for indicator_name in indicators:
                    try:
                        self.generator.set_data(self.source_data_name, 
                                                indicator_name, 
                                                dataset_name, 
                                                self.years,
                                                cache_directory = self.cache_directory)
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
                
                viz_args = self._get_viz_args(visualization_type, params, indicators)
                self.visualizer.run(args = viz_args, cache_directory = self.cache_directory)
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
    