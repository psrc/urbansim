# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE
        


import os
from inprocess.demo.utilities import indicator_to_XML_writer

#############################################################
#DEFINE indicators
#############################################################
from inprocess.travis.opus_core.indicator_framework.representations.indicator import Indicator

indicators = {
   'zone_population':Indicator( 
       dataset_name = 'zone',
       attribute = 'urbansim.zone.population'),   

   'gridcell_population':Indicator(
       dataset_name = 'gridcell',
       attribute = 'urbansim.gridcell.population'),  

   'gridcell_number_of_jobs':Indicator(
       dataset_name = 'gridcell',
       attribute = 'urbansim.gridcell.number_of_jobs', 
       name = 'jobs'),

   'zone_number_of_jobs':Indicator(
       dataset_name = 'zone',
       attribute = 'urbansim.zone.number_of_jobs', 
       name = 'zone_jobs'),

   'gridcell_industrial_sqft':Indicator(
       dataset_name = 'gridcell',
       attribute = 'urbansim.gridcell.industrial_sqft'), 
                        
   'zone_industrial_sqft':Indicator(
       dataset_name = 'zone',
       attribute = 'urbansim.zone.industrial_sqft'),  

   'gridcell_total_land_value':Indicator(
       dataset_name = 'gridcell',
       attribute = 'urbansim.gridcell.total_land_value'), 
                        
   'zone_total_land_value':Indicator(
       dataset_name = 'zone',
       attribute = 'urbansim.zone.total_land_value'),  
                         
   'gridcell_population_density':Indicator(
       dataset_name = 'gridcell',
       attribute = 'urbansim.gridcell.population_density'), 
                        
#   'zone_population_density':Indicator(
#       dataset_name = 'zone',
#       attribute = 'urbansim.zone.population_density'),
                   
}


#################################################################
#DEFINE data source
#################################################################
# define any number of cache directories and/or years 
# over which the indicators are computed
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from inprocess.travis.opus_core.indicator_framework.maker.source_data import SourceData

source_data = SourceData(
   cache_directory = os.path.join(os.environ['OPUS_DATA_PATH'],
                                  'eugene',
                                  'eugene_1980_baseyear_cache'),
   years = [1980],
   dataset_pool_configuration = DatasetPoolConfiguration(
         package_order=['eugene','urbansim','opus_core'],
         ),
   name = 'run_1090'
)

################################################################
#COMPUTE indicators
################################################################
# setup an indicator Maker that will compute a set of indicators
# for a given result template
from inprocess.travis.opus_core.indicator_framework.maker.maker import Maker

maker = Maker()
computed_indicators = maker.create_batch(
                            indicators = indicators, 
                            source_data = source_data)

print indicator_to_XML_writer(computed_indicators)

############################################
#VISUALIZE the resulting computed indicators
############################################
#from inprocess.travis.opus_core.indicator_framework.visualizer.visualization_factory import VisualizationFactory
#from opus_core.database_management.configurations.database_configuration import DatabaseConfiguration
#
#visualizer = VisualizationFactory()
#visualizations = []
#
## View an indicator as a matplotlib Map
#maps = ['gridcell_number_of_jobs',
#        'gridcell_population']
#visualizations += visualizer.visualize(
#    indicators_to_visualize = maps, #override default indicators to visualize (all)
#    computed_indicators = computed_indicators,
#    visualization_type = 'matplotlib_map',
#    name = 'my_maps'
#    )
#    
#    # View an indicator as a matplotlib Chart
#    
#    charts = ['alldata_home_based_jobs']
#    visualizations += visualizer.visualize(
#        indicators_to_visualize = charts,
#        computed_indicators = computed_indicators,
#        visualization_type = 'matplotlib_chart',
#        name = 'charts'
#        )
#
#    # Write an indicator as a Table
#    
#    from inprocess.travis.opus_core.indicator_framework.visualizer.visualizers.table import Table
#    
#    tables = ['zone_industrial_sqft', 
#              'large_area_population_change',
#              'alldata_home_based_jobs',
#              'gridcell_population',
#              'gridcell_number_of_jobs'
#              ]
#    for output_type in ['tab','csv']:#,'dbf']:
#        visualizations += visualizer.visualize(
#            indicators_to_visualize = tables,
#            computed_indicators = computed_indicators,
#            visualization_type = 'table',
#            output_type = output_type,
#            output_style = Table.PER_YEAR, 
#            name = 'tables',
#            )
    
# Write a set of indicators sharing a dataset as a Dataset Table

#indicators_in_dataset_table = ['zone_population',
#                               'zone_industrial_sqft']
#visualizations += visualizer.visualize(
#    indicators_to_visualize = indicators_in_dataset_table,
#    computed_indicators = computed_indicators,
#    visualization_type = 'dataset_table',
#    output_type = 'csv',
#    exclude_condition = 'urbansim.zone.population<100', #this accepts any opus expression
#    name = 'dataset_table',
#    )
#
#################################################################
##Generate a REPORT with the visualizations
#################################################################
#from inprocess.travis.opus_core.indicator_framework.reporter.report_factory import ReportFactory
#
#reporter = ReportFactory()
#reporter.generate_report(
#    visualized_indicators = visualizations,
#    report_type = 'basic',
#    open_immediately = True,
#    storage_location = 'c:/my_reports'                     
#)

