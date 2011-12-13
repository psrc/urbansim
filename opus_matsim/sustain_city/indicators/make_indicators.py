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
#cache_directory = r'/net/ils/nicolai3/opus_home/data/psrc_parcel/runs/run_4.2011_05_13_13_53' # highway limited cap.
cache_directory = r'/net/ils/nicolai2/opus_home/data/psrc_parcel/runs/run_4.2011_05_13_13_52' # highway
#cache_directory = r'/net/ils/nicolai/opus_home/data/psrc_parcel/runs/run_4.2011_05_13_13_47' # ferry

types = ['tab']

print "creating indicators ..."

indicators = {

    'residential_sqft_per_unit2':Indicator(
       dataset_name = 'zone',
       attribute = 'zone.aggregate(safe_array_divide(urbansim_parcel.building.building_sqft * urbansim_parcel.building.is_residential,building.residential_units), intermediates=[parcel])'),
    
    'residential_sqft_per_unit':Indicator(
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.building.building_sqft_per_unit * urbansim_parcel.building.is_residential, intermediates=[parcel])'),
    
    'building_sqft_per_unit':Indicator(
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.building.building_sqft_per_unit, intermediates=[parcel])'), 
    
    #Todo: building.sqft * is_residential (muessete bei Bridge hoeher sein)
    'residential_sqft':Indicator(
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.building.building_sqft * urbansim_parcel.building.is_residential, intermediates=[parcel])'), 
    
    'building_sqft':Indicator(
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.building.building_sqft, intermediates=[parcel])'),  
    
    'avg_residential_price_per_unit_in_zone':Indicator( # focus here
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.building.price_per_unit * urbansim_parcel.building.is_residential, function=sum, intermediates=[parcel]) / zone.aggregate(building.residential_units,intermediates=[parcel])'),  
        
    'avg_price_per_unit_in_zone':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.building.avg_price_per_unit_in_zone, intermediates=[parcel])'),
              
    'avg_price_per_sqft_in_zone':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.building.avg_price_per_sqft_in_zone, intermediates=[parcel])'),
              
    'existing_units':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.parcel.existing_units)'),
              
    'residential_unit_sqft':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(building.residential_units * building.sqft_per_unit, intermediates=[parcel])'),
    
    'is_land_use_type_vacant908':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.parcel.is_land_use_type_vacant)'),
    
    'is_land_use_type_single_family_residential908':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.parcel.is_land_use_type_single_family_residential)'),
              
    'is_land_use_type_multi_family_residential908':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.parcel.is_land_use_type_multi_family_residential)'),
              
    'price_per_residential_unit908':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.parcel.price_per_residential_unit)'),
              
    'total_price_per_residential_unit908':Indicator(
       dataset_name = 'alldata',
       attribute = 'alldata.aggregate_all(urbansim_parcel.parcel.price_per_residential_unit)'),
              
    'is_residential_land_use_type908':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.parcel.is_residential_land_use_type)'),
              
    'num_parcels908':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(parcel.parcel_id > 0)'),
              
    'num_parcels_undevelopable908':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(numpy.logical_and(parcel.parcel_id > 0, parcel.land_use_type_id == 27 ))'),
    
    'num_parcels_sfr908':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(numpy.logical_and(parcel.parcel_id > 0, parcel.land_use_type_id == 24 ))'),
              
    'num_parcels_mfr908':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(numpy.logical_and(parcel.parcel_id > 0, parcel.land_use_type_id == 14 ))'),
    
    'total_value_per_sqft':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.parcel.total_value_per_sqft)'),
              
    'improvement_value':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.parcel.improvement_value)'),
              
    'residential_units':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.parcel.residential_units)'),
    
    'landimprovement908':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(parcel.land_value + urbansim_parcel.parcel.improvement_value)'),
              
    'landvalue908':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(parcel.land_value * parcel.parcel_sqft, function=mean)'),
              
    'landvaluePSRC':Indicator( 
       dataset_name = 'alldata',
       attribute = 'alldata.aggregate_all(parcel.land_value * parcel.parcel_sqft, function=mean)'),  
    
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
    
    'total_building_type_multi_familiy_residential':Indicator( # mfr (condo residential, multi family residential)
       dataset_name = 'alldata',
       attribute = 'alldata.aggregate_all(urbansim_parcel.building.is_generic_building_type_2)'),
    
    'building_type_multi_familiy_residential':Indicator( # mfr (condo residential, multi family residential)
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.building.is_generic_building_type_2, intermediates=[parcel])'),
    
    'total_building_type_single_familiy_residential':Indicator( # new indicator
       dataset_name = 'alldata',
       attribute = 'alldata.aggregate_all(urbansim_parcel.building.is_generic_building_type_1)'),
    
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
       
    'total_vacant_sfrs':Indicator( # new indicator
       dataset_name = 'alldata',
       attribute = 'alldata.aggregate_all(urbansim_parcel.building.vacant_residential_units * urbansim_parcel.building.is_generic_building_type_1)'),
       
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
              
    'total_population':Indicator( # new indicator
       dataset_name = 'alldata',
       attribute = 'alldata.aggregate_all(urbansim_parcel.zone.population)'),  

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
              
    'total_income_per_person':Indicator( 
       dataset_name = 'alldata',
       attribute = 'safe_array_divide(alldata.aggregate_all(household.income), alldata.aggregate_all(household.persons))'),
              
    'zone_income_per_worker':Indicator( 
       dataset_name = 'zone',
       attribute = 'safe_array_divide(zone.aggregate(household.income, intermediates=[building, parcel]), zone.aggregate(household.workers, intermediates=[building, parcel]))'), #'zone.aggregate(household.income / household.workers, intermediates=[building, parcel])'),
       
    'zone_employment_within_30min_travel_time':Indicator( 
       dataset_name = 'zone',
       attribute = 'urbansim_parcel.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone'), 
       
    'unit_price':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.building.unit_price, intermediates=[parcel])'),
              
    'unit_price_parcel':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.parcel.unit_price)'),
              
    'unit_price_parcel_residential':Indicator( 
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.building.unit_price * urbansim_parcel.building.is_residential , intermediates=[parcel])'),
              
    'total_unit_price':Indicator( # new indicator
       dataset_name = 'alldata',
       attribute = 'alldata.aggregate_all(urbansim_parcel.building.unit_price)'),

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
   cache_directory = cache_directory,
   comparison_cache_directory = cache_directory,
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
        indicators_to_visualize = ['unit_price_parcel_residential'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'unit_price_parcel_residential',
        )

for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['unit_price_parcel'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'unit_price_parcel',
        )

for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['residential_sqft_per_unit2'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'residential_sqft_per_unit2',
        )

for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['residential_sqft_per_unit'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'residential_sqft_per_unit',
        )

for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['building_sqft_per_unit'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'building_sqft_per_unit',
        )

for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['residential_sqft'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'residential_sqft',
        )

for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['building_sqft'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'building_sqft',
        )

for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['avg_residential_price_per_unit_in_zone'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'avg_residential_price_per_unit_in_zone',
        )

for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['avg_price_per_sqft_in_zone'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'avg_price_per_sqft_in_zone',
        )
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['avg_price_per_unit_in_zone'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'avg_price_per_unit_in_zone',
        )

for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['existing_units'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'existing_units',
        )

for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['total_price_per_residential_unit908'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'total_price_per_residential_unit908',
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
        indicators_to_visualize = ['improvement_value'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'improvement_value',
        )
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['total_value_per_sqft'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'total_value_per_sqft',
        )

for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['is_land_use_type_vacant908'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'is_land_use_type_vacant908',
        )
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['is_land_use_type_single_family_residential908'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'is_land_use_type_single_family_residential908',
        )
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['is_land_use_type_multi_family_residential908'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'is_land_use_type_multi_family_residential908',
        )

for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['price_per_residential_unit908'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'price_per_residential_unit908',
        )
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['is_residential_land_use_type908'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'is_residential_land_use_type908',
        )
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['num_parcels908'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'num_parcels908',
        )
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['num_parcels_undevelopable908'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'num_parcels_undevelopable908',
        )
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['num_parcels_sfr908'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'num_parcels_sfr908',
        )
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['num_parcels_mfr908'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'num_parcels_mfr908',
        )
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['landimprovement908'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'landimprovement908',
        )

for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['landvaluePSRC'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'landvaluePSRC',
        )
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['landvalue908'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'landvalue908',
        )

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
        indicators_to_visualize = ['residential_unit_sqft'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'residential_unit_sqft',
        )    

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
        indicators_to_visualize = ['total_income_per_person'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'total_income_per_person',
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
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['total_unit_price'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'total_unit_price',
        )
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['total_population'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'total_population',
        )
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['total_building_type_single_familiy_residential'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'total_building_type_single_familiy_residential',
        )

for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['total_building_type_multi_familiy_residential'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'total_building_type_multi_familiy_residential',
        )
    
for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['total_vacant_sfrs'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'total_vacant_sfrs',
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
