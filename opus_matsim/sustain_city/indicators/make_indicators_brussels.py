# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE


#############################################################
#DEFINE indicators
#############################################################
from opus_gui.results_manager.run.indicator_framework.representations.indicator import Indicator
import time

start_time = time.time()

project_name = 'brussels_zone'
years_arr = [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010]

# cupum scenarios 2030 re-estimated
#cache_directory = r'/Users/thomas/Development/opus_home/data/brussels_zone/runs/run_76.base_case_run2' # base case
#cache_directory = r'/Users/thomas/Development/opus_home/data/brussels_zone/runs/run_77.test_case_run2' # test case

cache_directory = r'/Users/thomas/Development/opus_home/data/brussels_zone/runs/run_3.accessibility_base_case' # test case

types = ['tab']

print("creating indicators ...")

indicators = {
              
    'faz__autogenvar0':Indicator(
       dataset_name = 'faz',
       attribute = 'faz.aggregate(household.persons, intermediates=[zone])'),
              
    'zone__autogenvar1':Indicator(
       dataset_name = 'zone',
       attribute = 'zone.aggregate(household.persons)'),
              
    'faz__autogenvar2':Indicator(
       dataset_name = 'faz',
       attribute = 'faz.number_of_agents(household)'),
}

print("... done.")

#################################################################
#DEFINE data source
#################################################################
# define any number of cache directories and/or years 
# over which the indicators are computed
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_gui.results_manager.run.indicator_framework.maker.source_data import SourceData

print("creating result template ...")

result_template = SourceData(
   cache_directory = cache_directory,
   comparison_cache_directory = cache_directory,
   years = years_arr,
   dataset_pool_configuration = DatasetPoolConfiguration(
         package_order=['urbansim_zone', 'urbansim', 'psrc', 'opus_core'],
         ),
   name = project_name
)

print("... done.")

################################################################
#COMPUTE indicators
################################################################
# setup an indicator Maker that will compute a set of indicators
# for a given result template
from opus_gui.results_manager.run.indicator_framework.maker.maker import Maker

print("creating maker (to compute indicators) ...")

maker = Maker( project_name )
computed_indicators = maker.create_batch(
                            indicators = indicators, 
                            source_data = result_template)

print("... done.")

############################################
#VISUALIZE the resulting computed indicators
############################################
from opus_gui.results_manager.run.indicator_framework.visualizer.visualization_factory import VisualizationFactory
#from opus_core.database_management.configurations.database_configuration import DatabaseConfiguration

visualizer = VisualizationFactory()
visualizations = []

for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['faz__autogenvar0'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'faz__autogenvar0',
        )
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['faz__autogenvar2'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'faz__autogenvar2',
        )
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['zone__autogenvar1'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'zone__autogenvar1',
        )


end_time = time.time()

print("Computation took : %f\n" %(end_time-start_time))
print("Finished!!!")
