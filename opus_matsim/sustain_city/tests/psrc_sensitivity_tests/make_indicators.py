# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE


#############################################################
#DEFINE indicators
#############################################################
from opus_gui.results_manager.run.indicator_framework.representations.indicator import Indicator
import time

start_time = time.time()

project_name = 'psrc_parcel_cupum_preliminary'
years_arr = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]

#cache_dir = r'/Users/thomas/Development/opus_home/data/psrc_parcel_cupum_preliminary/runs/run_3.2011_01_17_09_37'
#cache_dir = r'/Users/thomas/Development/opus_home/data/seattle_parcel/runs/run_34.run_2011_01_18_09_31'
cache_dir = r'/net/ils/nicolai/opus_home/data/psrc_parcel_cupum_preliminary/runs/ferry_mit_worklogsum_mitELCM'
#cache_dir = r'/net/ils/nicolai/opus_home/data/psrc_parcel_cupum_preliminary/runs/highway_ohne_worklogsum_ohneELCM'
#cache_dir = r'/net/ils/nicolai/opus_home/data/psrc_parcel_cupum_preliminary/runs/ferry_ohne_worklogsum_ohneELCM'
#cache_dir = r'/net/ils/nicolai/opus_home/data/psrc_parcel_cupum_preliminary/runs/highway_ohne_worklogsum_ohneELCM'
types = ['tab']

indicators = {
    
    'zone_travel_time_to_cbd':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.travel_time_to_cbd'),   
              
   'zone_population':Indicator( 
       dataset_name = 'zone',
       attribute = 'urbansim_parcel.zone.population'),  
       
    'zone_household_workers':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(household.workers)'),  
       
    'zone_household_persons':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(household.persons)'),
       
    'zone_fraction_household_workers_persons':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(household.workers/household.persons)'),  
       
    'zone_number_of_households':Indicator( 
       dataset_name = 'zone',
       attribute = 'urbansim_parcel.zone.number_of_households'),  
       
    'zone_income_per_person':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(household.income / household.persons)'),
       
    'zone_household_avg_income':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(household.income, function=mean)'),
       
    'zone_income_household':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(household.income)'),
       
    'zone_employment_within_30min_travel_time':Indicator( 
       dataset_name = 'zone',
       attribute = 'urbansim_parcel.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone'),
       
    'traveldata_am_single_vehicle_to_work_travel_time':Indicator( 
       dataset_name = 'travel_data',
       attribute = 'travel_data.am_single_vehicle_to_work_travel_time'),
       
    'travel_time_to_129':Indicator( 
       dataset_name = 'zone',
       attribute = 'psrc.zone.travel_time_hbw_am_drive_alone_to_cbd'),
       
    'travel_time_to_908':Indicator( 
       dataset_name = 'zone',
       attribute = 'psrc.zone.travel_time_hbw_am_drive_alone_to_908'),

   #'gridcell_population':Indicator(
   #    dataset_name = 'gridcell',
   #    attribute = 'urbansim.gridcell.population'),  
   
   #'zone_industrial_sqft':Indicator(
   #    dataset_name = 'zone',
   #    attribute = 'urbansim.zone.industrial_sqft'),  
              
   #'gridcell_number_of_jobs':Indicator(
   #    dataset_name = 'gridcell',
   #    attribute = 'urbansim.gridcell.number_of_jobs', 
   #    name = 'jobs'),

   #'zone_number_of_jobs':Indicator(
   #    dataset_name = 'zone',
   #    attribute = 'urbansim.gridcell.number_of_jobs', 
   #    name = 'zone_jobs'),
              
   #Expression example (comparison to baseyear)
   #'large_area_population_change':Indicator(
   #    dataset_name = 'large_area',
   #    name = 'de_population_change',
   #    attribute = 'psrc.large_area.de_population_DDDD - psrc.large_area.de_population_2000',
   #),

   #example using regional-level aggregators
   #'alldata_home_based_jobs':Indicator(
   #    attribute = 'alldata.aggregate_all(urbansim.zone.number_of_home_based_jobs)',
   #    dataset_name = 'alldata',
   #    name =  'number_of_home_based_jobs'),              
}


#################################################################
#DEFINE data source
#################################################################
# define any number of cache directories and/or years 
# over which the indicators are computed
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_gui.results_manager.run.indicator_framework.maker.source_data import SourceData

result_template = SourceData(
   cache_directory = cache_dir,
   comparison_cache_directory = cache_dir,
   years = years_arr,
   dataset_pool_configuration = DatasetPoolConfiguration(
         package_order=['urbansim_parcel','urbansim', 'psrc', 'opus_core'],
         ),
   name = project_name
)

################################################################
#COMPUTE indicators
################################################################
# setup an indicator Maker that will compute a set of indicators
# for a given result template
from opus_gui.results_manager.run.indicator_framework.maker.maker import Maker

maker = Maker( project_name )
computed_indicators = maker.create_batch(
                            indicators = indicators, 
                            source_data = result_template)

############################################
#VISUALIZE the resulting computed indicators
############################################
from opus_gui.results_manager.run.indicator_framework.visualizer.visualization_factory import VisualizationFactory
#from opus_core.database_management.configurations.database_configuration import DatabaseConfiguration

visualizer = VisualizationFactory()
visualizations = []

# View an indicator as a Map
#maps = ['zone_population',
#        'gridcell_population']
#visualizations += visualizer.visualize(
#    indicators_to_visualize = maps, #override default indicators to visualize (all)
#    computed_indicators = computed_indicators,
#    visualization_type = 'mapnik_map',
#    name = 'my_maps'
#    )

# View an indicator as a matplotlib Chart

#charts = ['gridcell_population']
#visualizations += visualizer.visualize(
#    indicators_to_visualize = charts,
#    computed_indicators = computed_indicators,
#    visualization_type = 'matplotlib_chart',
#    years = [2010], #override default years to visualize (all)
#    name = 'charts'
#    )

# Write an indicator as a Table

for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['zone_travel_time_to_cbd'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'zone_travel_time_to_cbd',
        )
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['zone_population'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'zone_population',
        )
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['zone_household_workers'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'zone_household_workers',
        )
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['zone_household_persons'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'zone_household_persons',
        )

for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['zone_household_avg_income'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'zone_household_avg_income',
        )

for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['zone_fraction_household_workers_persons'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'zone_fraction_household_workers_persons',
        )
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['zone_number_of_households'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'zone_number_of_households',
        )
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['zone_income_per_person'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'zone_income_per_person',
        )
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['zone_income_household'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'zone_income_household',
        )
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['travel_time_to_129'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'travel_time_to_129',
        )
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['travel_time_to_908'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'travel_time_to_908',
        )
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['zone_employment_within_30min_travel_time'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'zone_employment_within_30min_travel_time',
        )
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['traveldata_am_single_vehicle_to_work_travel_time'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'traveldata_am_single_vehicle_to_work_travel_time',
        )
    
    
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

################################################################
#Generate a REPORT with the visualizations
################################################################
#from opus_gui.results_manager.run.indicator_framework.reporter.report_factory import ReportFactory

#reporter = ReportFactory()
#reporter.generate_report(
#    visualized_indicators = visualized_indicators,
#    report_type = 'basic',
#    open_immediately = True,
#    storage_location = 'c:/my_reports'                     
#)

end_time = time.time()

print "Computation took : %f\n" %(end_time-start_time)
print "Finished!!!"
