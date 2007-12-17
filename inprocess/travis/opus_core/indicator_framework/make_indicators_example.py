#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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


#############################################################
#DEFINE indicators
#############################################################
from inprocess.travis.opus_core.indicator_framework.maker.indicator import Indicator

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
from inprocess.travis.opus_core.indicator_framework.maker.source_data import SourceData

result_template = SourceData(
   cache_directory = r'D:\urbansim_cache\run_1090.2006_11_14_12_12',
   comparison_cache_directory = r'D:\urbansim_cache\run_1091.2006_11_14_12_12',
   years = [2000, 2010],
   dataset_pool_configuration = DatasetPoolConfiguration(
         package_order=['urbansim','opus_core'],
         package_order_exceptions={},
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
                            result_template = result_template)

############################################
#VISUALIZE the resulting computed indicators
############################################
from inprocess.travis.opus_core.indicator_framework.visualizer.visualization_factory import VisualizationFactory
from opus_core.database_management.database_configuration import DatabaseConfiguration

visualizer = VisualizationFactory()
visualized_indicators = []

# View an indicator as a matplotlib Map
maps = ['zone_population',
        'gridcell_population']
visualized_indicators += visualizer.visualize(
    indicators_to_visualize = maps, #override default indicators to visualize (all)
    computed_indicators = computed_indicators,
    visualization_type = 'matplotlib_map',
    )

# View an indicator as a matplotlib Chart

charts = ['gridcell_population']
visualized_indicators += visualizer.visualize(
    indicators_to_visualize = charts,
    computed_indicators = computed_indicators,
    visualization_type = 'matplotlib_chart',
    years = [2010] #override default years to visualize (all)
    )

# Write an indicator as a Table

tables = ['zone_industrial_sqft', 
          'large_area_population_change',
          'alldata_home_based_jobs']
for output_type in ['tab','cvs','dbf']:
    visualized_indicators += visualizer.visualize(
        indicators_to_visualize = tables,
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type
        )
    
# Write a set of indicators sharing a dataset as a Dataset Table

indicators_in_dataset_table = ['zone_population',
                               'zone_industrial_sqft']
visualized_indicators += visualizer.visualize(
    indicators_to_visualize = indicators_in_dataset_table,
    computed_indicators = computed_indicators,
    visualization_type = 'dataset_table',
    output_type = 'csv',
    exclude_condition = 'urbansim.zone.population<100' #this accepts any opus expression
    )    

################################################################
#Generate a REPORT with the visualizations
################################################################
from inprocess.travis.opus_core.indicator_framework.reporter.report_factory import ReportFactory

reporter = ReportFactory
reporter.generate_report(
    indicators_in_report = visualized_indicators,
    report_type = 'basic',
    open_immediately = True,
    storage_location = 'c:/my_reports'                     
)
