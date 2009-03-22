# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE


#############################################################
#DEFINE indicators
#############################################################
from opus_gui.results_manager.run.indicator_framework.maker.indicator import Indicator

indicators = {
   'zone_population':Indicator( 
       dataset_name = 'zone',
       attribute = 'urbansim.zone.population'),   

   'gridcell_population':Indicator(
       dataset_name = 'gridcell',
       attribute = 'urbansim.gridcell.population'),  
   
   'zone_industrial_sqft':Indicator(
       dataset_name = 'zone',
       attribute = 'urbansim.zone.industrial_sqft'),  
              
   'gridcell_number_of_jobs':Indicator(
       dataset_name = 'gridcell',
       attribute = 'urbansim.gridcell.number_of_jobs', 
       name = 'jobs'),

   'zone_number_of_jobs':Indicator(
       dataset_name = 'zone',
       attribute = 'urbansim.gridcell.number_of_jobs', 
       name = 'zone_jobs'),
              
   #Expression example (comparison to baseyear)
   'large_area_population_change':Indicator(
       dataset_name = 'large_area',
       name = 'de_population_change',
       attribute = 'psrc.large_area.de_population_DDDD - psrc.large_area.de_population_2000',
   ),

   #example using regional-level aggregators
   'alldata_home_based_jobs':Indicator(
       attribute = 'alldata.aggregate_all(urbansim.zone.number_of_home_based_jobs)',
       dataset_name = 'alldata',
       name =  'number_of_home_based_jobs'),              
}


#################################################################
#DEFINE data source
#################################################################
# define any number of cache directories and/or years 
# over which the indicators are computed
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_gui.results_manager.run.indicator_framework.maker.source_data import SourceData

result_template = SourceData(
   cache_directory = r'D:\urbansim_cache\run_1090.2006_11_14_12_12',
   comparison_cache_directory = r'D:\urbansim_cache\run_1091.2006_11_14_12_12',
   years = [2000, 2010],
   dataset_pool_configuration = DatasetPoolConfiguration(
         package_order=['urbansim','opus_core'],
         ),
   name = 'run_1090'
)

################################################################
#COMPUTE indicators
################################################################
# setup an indicator Maker that will compute a set of indicators
# for a given result template
from opus_gui.results_manager.run.indicator_framework.maker.maker import Maker

maker = Maker()
computed_indicators = maker.create_batch(
                            indicators = indicators, 
                            result_template = result_template)

############################################
#VISUALIZE the resulting computed indicators
############################################
from opus_gui.results_manager.run.indicator_framework.visualizer.visualization_factory import VisualizationFactory
from opus_core.database_management.configurations.database_configuration import DatabaseConfiguration

visualizer = VisualizationFactory()
visualizations = []

# View an indicator as a Map
maps = ['zone_population',
        'gridcell_population']
visualizations += visualizer.visualize(
    indicators_to_visualize = maps, #override default indicators to visualize (all)
    computed_indicators = computed_indicators,
    #visualization_type = 'matplotlib_map',
    visualization_type = 'mapnik_map',
    name = 'my_maps'
    )

# View an indicator as a matplotlib Chart

charts = ['gridcell_population']
visualizations += visualizer.visualize(
    indicators_to_visualize = charts,
    computed_indicators = computed_indicators,
    visualization_type = 'matplotlib_chart',
    years = [2010], #override default years to visualize (all)
    name = 'charts'
    )

# Write an indicator as a Table

tables = ['zone_industrial_sqft', 
          'large_area_population_change',
          'alldata_home_based_jobs']
for output_type in ['tab','cvs','dbf']:
    visualizations += visualizer.visualize(
        indicators_to_visualize = tables,
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'tables',
        )
    
# Write a set of indicators sharing a dataset as a Dataset Table

indicators_in_dataset_table = ['zone_population',
                               'zone_industrial_sqft']
visualizations += visualizer.visualize(
    indicators_to_visualize = indicators_in_dataset_table,
    computed_indicators = computed_indicators,
    visualization_type = 'dataset_table',
    output_type = 'csv',
    exclude_condition = 'urbansim.zone.population<100' #this accepts any opus expression
    name = 'dataset_table',
    )

################################################################
#Generate a REPORT with the visualizations
################################################################
from opus_gui.results_manager.run.indicator_framework.reporter.report_factory import ReportFactory

reporter = ReportFactory()
reporter.generate_report(
    visualized_indicators = visualized_indicators,
    report_type = 'basic',
    open_immediately = True,
    storage_location = 'c:/my_reports'                     
)
