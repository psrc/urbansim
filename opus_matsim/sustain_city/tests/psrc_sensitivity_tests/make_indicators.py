# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE


#############################################################
#DEFINE indicators
#############################################################
from opus_gui.results_manager.run.indicator_framework.representations.indicator import Indicator
import time

start_time = time.time()

project_name = 'psrc_parcel'
years_arr = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030]

# cupum scenarios 2030 re-estimated
cache_dir = r'/net/ils/nicolai3/opus_home/data/psrc_parcel/runs/run_5.2011_05_02_15_18' # highway limited cap.
#cache_dir = r'/net/ils/nicolai2/opus_home/data/psrc_parcel/runs/run_5.2011_05_02_14_41' # highway
#cache_dir = r'/net/ils/nicolai/opus_home/data/psrc_parcel/runs/run_5.2011_05_02_14_37' # ferry

# cupum scenarios 2030 
#cache_dir = r'/net/ils/nicolai/opus_home/data/psrc_parcel/runs/run_2.2011_02_25_19_21' # highway limited cap.
#cache_dir = r'/net/ils/nicolai/opus_home/data/psrc_parcel/runs/run_1.2011_02_24_11_54' # highway
#cache_dir = r'/net/ils/nicolai2/opus_home/data/psrc_parcel/runs/run_1.2011_02_24_11_55' # ferry

types = ['tab']

print "creating indicators ..."

indicators = {
    
    'building_type_other':Indicator( # other (agriculture, group_quarter, out building, open space, parking, recreation, school, no code)
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.building.is_generic_building_type_8, intermediates=[parcel])'),

    'building_type_government':Indicator( # government (civic an quasi public, government, hospital, military)
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.building.is_generic_building_type_7, intermediates=[parcel])'),

    'building_type_mixed-use':Indicator( # mixed-use
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.building.is_generic_building_type_6, intermediates=[parcel])'),

    'building_type_industrial':Indicator( # industrial (industrial, transportation ,Communication, Warehousing)
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.building.is_generic_building_type_5, intermediates=[parcel])'),

    'building_type_commercial':Indicator( # commercial
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.building.is_generic_building_type_4, intermediates=[parcel])'),
       
    'building_type_office':Indicator( # office
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.building.is_generic_building_type_3, intermediates=[parcel])'),
    
    'building_type_multi_familiy_residential':Indicator( # mfr (condo residential, multi family residential)
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.building.is_generic_building_type_2, intermediates=[parcel])'),
       
    'building_type_single_familiy_residential':Indicator( # sfr (mobile home, single family residential)
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.building.is_generic_building_type_1, intermediates=[parcel])'),

    'single_familiy_housing_units':Indicator( # sfr (mobile home, single family residential)
       dataset_name = 'zone',
       attribute = 'zone.aggregate(building.residential_units * urbansim_parcel.building.is_generic_building_type_1)'),
       
    'multi_familiy_housing_units':Indicator( # mfr (condo residential, multi family residential)
       dataset_name = 'zone',
       attribute = 'zone.aggregate(building.residential_units * urbansim_parcel.building.is_generic_building_type_2)'),
       
    'office_sqft':Indicator( # office
       dataset_name = 'zone',
       attribute = 'zone.aggregate(building.non_residential_sqft * urbansim_parcel.building.is_generic_building_type_3)'),
       
    'commercial_sqft':Indicator( # commercial
       dataset_name = 'zone',
       attribute = 'zone.aggregate(building.non_residential_sqft * urbansim_parcel.building.is_generic_building_type_4)'),

    'industrial_sqft':Indicator( # industrial (industrial, transportation ,Communication, Warehousing)
       dataset_name = 'zone',
       attribute = 'zone.aggregate(building.non_residential_sqft * urbansim_parcel.building.is_generic_building_type_5)'),
       
    'other_sqft':Indicator( # other (agriculture, group_quarter, outbuilding, open space, parking, recreation, school, no code)
       dataset_name = 'zone',
       attribute = 'zone.aggregate(building.non_residential_sqft * urbansim_parcel.building.is_generic_building_type_7)'),

    'vacant_residential_units':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.building.vacant_residential_units)'),
       
    'vacant_sfrs':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.building.vacant_residential_units * urbansim_parcel.building.is_generic_building_type_1)'),

    'vacant_mfrs':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.building.vacant_residential_units * urbansim_parcel.building.is_generic_building_type_2)'),

    'travel_time_to_129':Indicator( 
       dataset_name = 'zone',
       attribute = 'psrc.zone.travel_time_hbw_am_drive_alone_to_cbd'),
              
   'zone_population':Indicator( 
       dataset_name = 'zone',
       attribute = 'urbansim_parcel.zone.population'),  

    'zone_household_workers':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(household.workers, intermediates=[building, parcel])'),  
       
    'zone_number_of_households':Indicator( 
       dataset_name = 'zone',
       attribute = 'urbansim_parcel.zone.number_of_households'),
       
    #'zone_number_of_residential_units':Indicator( 
    #   dataset_name = 'zone',
    #   attribute = 'urbansim_parcel.building.residential_units'),
       
    'zone_number_of_single_households':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(household.persons == 1, intermediates=[building, parcel])'),
       
    'zone_income_per_person':Indicator( 
       dataset_name = 'zone',
       attribute = 'safe_array_divide(zone.aggregate(household.income, intermediates=[building, parcel]), zone.aggregate(household.persons, intermediates=[building, parcel]))'),  #'zone.aggregate(household.income / household.persons, intermediates=[building, parcel])'),
       
    'zone_income_per_worker':Indicator( 
       dataset_name = 'zone',
       attribute = 'safe_array_divide(zone.aggregate(household.income, intermediates=[building, parcel]), zone.aggregate(household.workers, intermediates=[building, parcel]))'), #'zone.aggregate(household.income / household.workers, intermediates=[building, parcel])'),
       
    'zone_employment_within_30min_travel_time':Indicator( 
       dataset_name = 'zone',
       attribute = 'urbansim_parcel.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone'), 
       
    'unit_price':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.building.unit_price, intermediates=[parcel])'),

    'number_of_jobs':Indicator( 
       dataset_name = 'zone',
       attribute = 'urbansim_parcel.zone.number_of_jobs'),
       
    'number_of_buildings':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(building.building_id > 0, intermediates=[parcel])'),

    'vacant_land_area':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.parcel.vacant_land_area)'),
       
    'residential_units':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(building.residential_units, intermediates=[parcel])'),
       
    'total_units':Indicator( 
       dataset_name = 'alldata',
       attribute = 'alldata.aggregate_all(building.residential_units * urbansim_parcel.building.is_generic_building_type_1)'),

    'total_office_units':Indicator( 
       dataset_name = 'alldata',
       attribute = 'alldata.aggregate_all(building.non_residential_sqft * urbansim_parcel.building.is_generic_building_type_3)'),

    #'building_sqft_per_unit':Indicator( 
    #   dataset_name = 'zone',
    #   attribute = 'safe_array_divide(zone.aggregate(building.non_residential_sqft * urbansim_parcel.building.is_residential),  zone.aggregate(building.residential_units * urbansim_parcel.building.is_residential))'),

    'worker_share':Indicator( 
       dataset_name = 'zone',
       attribute = 'safe_array_divide(zone.aggregate(household.workers, intermediates=[building, parcel]), urbansim_parcel.zone.population)'),

    'single_hh_share':Indicator( 
       dataset_name = 'zone',
       attribute = 'safe_array_divide(zone.aggregate(household.persons == 1, intermediates=[building, parcel]), urbansim_parcel.zone.number_of_households)'),

    #'building_sqft_per_unit':Indicator( 
    #   dataset_name = 'zone',
    #   attribute = 'zone.aggregate(urbansim_parcel.building.building_sqft_per_unit, intermediates=[parcel])'),

    #'building_sqft_per_job':Indicator( 
    #   dataset_name = 'zone',
    #   attribute = 'zone.aggregate(urbansim_parcel.building.building_sqft_per_job, intermediates=[parcel])'),

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

print "... done."

#################################################################
#DEFINE data source
#################################################################
# define any number of cache directories and/or years 
# over which the indicators are computed
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_gui.results_manager.run.indicator_framework.maker.source_data import SourceData

print "creating result template ..."

result_template = SourceData(
   cache_directory = cache_dir,
   comparison_cache_directory = cache_dir,
   years = years_arr,
   dataset_pool_configuration = DatasetPoolConfiguration(
         package_order=['urbansim_parcel', 'urbansim', 'psrc', 'opus_core'],
         ),
   name = project_name
)

print "... done."

################################################################
#COMPUTE indicators
################################################################
# setup an indicator Maker that will compute a set of indicators
# for a given result template
from opus_gui.results_manager.run.indicator_framework.maker.maker import Maker

print "creating maker (to compute indicators) ..."

maker = Maker( project_name )
computed_indicators = maker.create_batch(
                            indicators = indicators, 
                            source_data = result_template)

print "... done."

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

#for output_type in types:
#    visualizations += visualizer.visualize(
#        indicators_to_visualize = ['avg_work_logsum'],
#        computed_indicators = computed_indicators,
#        visualization_type = 'table',
#        output_type = output_type,
#        name = 'avg_work_logsum',
#        )

for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['building_type_single_familiy_residential'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'building_type_single_familiy_residential',
        )
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['building_type_multi_familiy_residential'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'building_type_multi_familiy_residential',
        )

for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['building_type_office'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'building_type_office',
        )

for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['building_type_commercial'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'building_type_commercial',
        )

for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['building_type_industrial'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'building_type_industrial',
        )

for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['building_type_mixed-use'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'building_type_mixed-use',
        )

for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['building_type_government'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'building_type_government',
        )

for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['building_type_other'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'building_type_other',
        )
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['number_of_buildings'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'number_of_buildings',
        )
    
#for output_type in types:
#    visualizations += visualizer.visualize(
#        indicators_to_visualize = ['zone_number_of_residential_units'],
#        computed_indicators = computed_indicators,
#        visualization_type = 'table',
#        output_type = output_type,
#        name = 'zone_number_of_residential_units',
#        )
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['single_familiy_housing_units'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'single_familiy_housing_units',
        )
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['multi_familiy_housing_units'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'multi_familiy_housing_units',
        )
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['office_sqft'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'office_sqft',
        )
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['commercial_sqft'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'commercial_sqft',
        )
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['industrial_sqft'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'industrial_sqft',
        )
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['other_sqft'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
       name = 'other_sqft',
        )
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['vacant_residential_units'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'vacant_residential_units',
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
        indicators_to_visualize = ['zone_number_of_households'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'zone_number_of_households',
        )
        
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['zone_number_of_single_households'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'zone_number_of_single_households',
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
        indicators_to_visualize = ['zone_income_per_worker'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'zone_income_per_worker',
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
        indicators_to_visualize = ['unit_price'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'unit_price',
        )

for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['number_of_jobs'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'number_of_jobs',
        )

for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['vacant_land_area'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'vacant_land_area',
        )

for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['residential_units'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'residential_units',
        )    

for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['vacant_sfrs'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'vacant_sfrs',
        )
   
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['vacant_mfrs'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'vacant_mfrs',
        )

for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['total_units'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'total_units',
        )
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['total_office_units'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'total_office_units',
        )
    
#for output_type in types:
#    visualizations += visualizer.visualize(
#        indicators_to_visualize = ['building_sqft_per_unit'],
#        computed_indicators = computed_indicators,
#        visualization_type = 'table',
#        output_type = output_type,
#        name = 'building_sqft_per_unit',
#        )  
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['worker_share'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'worker_share',
        ) 
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['single_hh_share'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'single_hh_share',
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
