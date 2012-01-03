# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE


#############################################################
#DEFINE indicators
#############################################################
import os
from opus_gui.results_manager.run.indicator_framework.representations.indicator import Indicator

project_name = pn = 'zurich_parcel'
# setting project name to environment. this is needed for the visualizer
os.environ['OPUSPROJECTNAME'] = pn

years_arr = [2000,2002,2004,2006,2008,2010]
# zurich scenario from 2000 to 2010
#cache_directory = r'/Users/sustaincity/Development/opus_home/data/zurich_parcel_from_20111014/results/dec2011/run_3.test_no_action_1pct_30it_2000-2010_warm-hot-start'
#cache_directory = r'/Users/sustaincity/Development/opus_home/data/zurich_parcel_from_20111014/results/dec2011/run_4.test_schwamendingertunnel_1pct_30it_2000-2010_war-hot-start'
#cache_directory = r'/Users/sustaincity/Development/opus_home/data/zurich_parcel_from_20111014/results/dec2011/run_5.test_no_action_with_accessibility_1pct_30it_2000-2010_warm-hot-start'
cache_directory = r'/Users/sustaincity/Development/opus_home/data/zurich_parcel_from_20111014/results/dec2011/run_6.test_schwamendingertunnel_with_accessibility_1pct_30it_2000-2010_warm-hot-start'

print "creating indicators for %s" % os.environ['OPUSPROJECTNAME']

indicators = {
    
    'population':Indicator(
        dataset_name = 'zone',
        attribute = 'zone.aggregate(household.persons, intermediates=[building,parcel])' ),
    'income_per_person':Indicator( 
       dataset_name = 'zone',
       attribute = 'safe_array_divide(zone.aggregate(household.income, intermediates=[building,parcel]), zone.aggregate(household.persons, intermediates=[building,parcel]))'),
            
    # No further division into single family or multi family residential!  (Wohngebaeude)
    'residential_units':Indicator(
        dataset_name = 'zone',
        attribute = 'zone.aggregate(building.residential_units, intermediates=[parcel])' ),
    'price_per_residential_unit':Indicator( # see urbansim_parcel.parcel.price_per_residential_unit
        dataset_name = 'zone',
        attribute = 'zone.aggregate( safe_array_divide( parcel.land_value + parcel.aggregate(building.improvement_value) , parcel.aggregate(building.residential_units) ) )' ),
    'price_per_residential_sqft':Indicator(
        dataset_name = 'zone',
        attribute = 'zone.aggregate( safe_array_divide( parcel.land_value + parcel.aggregate(building.improvement_value) , parcel.aggregate(building.residential_units * building.sqft_per_unit) ) )' ),
    'parcel_price_per_residential_unit':Indicator(
        dataset_name = 'parcel',
        attribute = 'safe_array_divide( parcel.land_value + parcel.aggregate(building.improvement_value), parcel.aggregate(building.residential_units) )' ),
    'parcel_price_per_residential_sqft':Indicator(
        dataset_name = 'parcel',
        attribute = 'safe_array_divide( parcel.land_value + parcel.aggregate(building.improvement_value), parcel.aggregate(building.residential_units * building.sqft_per_unit))' ),
    # tnicolai: does not work, missing "land_use_type_id" attribute
    #'unit_price':Indicator( 
    #   dataset_name = 'zone',
    #   attribute = 'zone.aggregate(urbansim_parcel.parcel.unit_price)'),
    #'unit_price_residential':Indicator( 
    #   dataset_name = 'zone',
    #   attribute = 'zone.aggregate(urbansim_parcel.building.unit_price * urbansim_parcel.building.is_residential , intermediates=[parcel])'),    
     
     # Verwaltung
    'admin_sqft':Indicator(
        dataset_name = 'zone',
        attribute = 'zone.aggregate(building.non_residential_sqft * (building.building_type_id==0))' ),
    # Land, Forst, Garten
    'green_areas_sqft':Indicator(
        dataset_name = 'zone',
        attribute = 'zone.aggregate(building.non_residential_sqft * (building.building_type_id==2))' ),
     # transport
    'transport_sqft':Indicator(
        dataset_name = 'zone',
        attribute = 'zone.aggregate(building.non_residential_sqft * (building.building_type_id==3))' ),
     # Handel
    'commerce_sqft':Indicator(
        dataset_name = 'zone',
        attribute = 'zone.aggregate(building.non_residential_sqft * (building.building_type_id==4))' ),
     # Industriegewerbe
    'industry_sqft':Indicator(
        dataset_name = 'zone',
        attribute = 'zone.aggregate(building.non_residential_sqft * (building.building_type_id==5))' ),
     # Gastronomie
    'gastronomy_sqft':Indicator(
        dataset_name = 'zone',
        attribute = 'zone.aggregate(building.non_residential_sqft * (building.building_type_id==6))' ),
     # Nebengebaeude (what type ?)
    'out_building_sqft':Indicator(
        dataset_name = 'zone',
        attribute = 'zone.aggregate(building.non_residential_sqft * (building.building_type_id==7))' ),
    
    # misc
    'number_of_jobs':Indicator(
        dataset_name = 'zone',
        attribute = 'urbansim_parcel.zone.number_of_jobs' ),
    'number_of_households':Indicator(
        dataset_name = 'zone',
        attribute = 'urbansim_parcel.zone.number_of_households' ),
    'average_household_income':Indicator(
        dataset_name = 'zone',
        attribute = 'urbansim_parcel.zone.average_household_income' ),
    'used_land_area':Indicator(
        dataset_name = 'zone',
        attribute = 'zone.aggregate(urbansim_parcel.parcel.used_land_area)' ),
    'vacant_land_area':Indicator(
        dataset_name = 'zone',
        attribute = 'zone.aggregate(urbansim_parcel.parcel.vacant_land_area)' ),
    'demolition_cost':Indicator(
        dataset_name = 'zone',
        attribute = 'zone.aggregate(urbansim_parcel.building.demolition_cost, intermediates=[building,parcel])' ),
              
    # travel time dependent indicators
    'employment_within_10_minutes_travel_time_hbw_am_drive_alone':Indicator(
        dataset_name = 'zone',
        attribute = 'urbansim_parcel.zone.employment_within_10_minutes_travel_time_hbw_am_drive_alone' ),
    'employment_within_30_minutes_travel_time_hbw_am_drive_alone':Indicator(
        dataset_name = 'zone',
        attribute = 'urbansim_parcel.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone' ),
    'travel_time_to_611':Indicator( # in zone 611 is the main station 
       dataset_name = 'zone',
       attribute = 'psrc.zone.travel_time_hbw_am_drive_alone_to_611'),
    'travel_time_accessibility':Indicator( # in zone 611 is the main station 
       dataset_name = 'zone',
       attribute = 'zone.travel_time_accessibility'),
              
    # land variables
    'improvement_value':Indicator(
       dataset_name = 'zone',
       attribute = 'zone.aggregate(urbansim_parcel.parcel.improvement_value)'),
           
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

source_data = SourceData(
   cache_directory = cache_directory,
   #comparison_cache_directory = cache_directory,
   years = years_arr,
   dataset_pool_configuration = DatasetPoolConfiguration(
         package_order=['urbansim_zone', 'urbansim_parcel', 'urbansim', 'psrc', 'opus_core'],
         ),
   #name = project_name
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
                            source_data = source_data)
print "... done."

############################################
#VISUALIZE the resulting computed indicators
############################################
from opus_gui.results_manager.run.indicator_framework.visualizer.visualization_factory import VisualizationFactory
# from opus_core.database_management.configurations.database_configuration import DatabaseConfiguration

visualizer = VisualizationFactory()
visualizations = []

# View an indicator as a Map
visualizations += visualizer.visualize(
    indicators_to_visualize = ['population'],
    computed_indicators = computed_indicators,
    visualization_type = 'mapnik_map',
    #name = 'population'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['income_per_person'],
    computed_indicators = computed_indicators,
    visualization_type = 'mapnik_map',
    #name = 'population'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['residential_units'], 
    computed_indicators = computed_indicators,
    visualization_type = 'mapnik_map',
    #name = 'residential_units'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['price_per_residential_unit'], 
    computed_indicators = computed_indicators,
    visualization_type = 'mapnik_map',
    #name = 'price_per_residential_unit'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['price_per_residential_sqft'], 
    computed_indicators = computed_indicators,
    visualization_type = 'mapnik_map',
    #name = 'price_per_residential_unit'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['admin_sqft'], 
    computed_indicators = computed_indicators,
    visualization_type = 'mapnik_map',
    #name = 'admin_sqft'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['green_areas_sqft'], 
    computed_indicators = computed_indicators,
    visualization_type = 'mapnik_map',
    #name = 'admin_sqft'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['transport_sqft'], 
    computed_indicators = computed_indicators,
    visualization_type = 'mapnik_map',
    #name = 'admin_sqft'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['commerce_sqft'], 
    computed_indicators = computed_indicators,
    visualization_type = 'mapnik_map',
    #name = 'admin_sqft'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['industry_sqft'], 
    computed_indicators = computed_indicators,
    visualization_type = 'mapnik_map',
    #name = 'admin_sqft'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['gastronomy_sqft'], 
    computed_indicators = computed_indicators,
    visualization_type = 'mapnik_map',
    #name = 'admin_sqft'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['out_building_sqft'], 
    computed_indicators = computed_indicators,
    visualization_type = 'mapnik_map',
    #name = 'admin_sqft'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['number_of_jobs'], 
    computed_indicators = computed_indicators,
    visualization_type = 'mapnik_map',
    #name = 'number_of_jobs'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['number_of_households'], 
    computed_indicators = computed_indicators,
    visualization_type = 'mapnik_map',
    #name = 'number_of_households'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['average_household_income'],
    computed_indicators = computed_indicators,
    visualization_type = 'mapnik_map',
    #name = 'average_income'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['used_land_area'],
    computed_indicators = computed_indicators,
    visualization_type = 'mapnik_map',
    #name = 'average_income'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['vacant_land_area'],
    computed_indicators = computed_indicators,
    visualization_type = 'mapnik_map',
    #name = 'average_income'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['demolition_cost'],
    computed_indicators = computed_indicators,
    visualization_type = 'mapnik_map',
    #name = 'average_income'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['employment_within_10_minutes_travel_time_hbw_am_drive_alone'], 
    computed_indicators = computed_indicators,
    visualization_type = 'mapnik_map',
    #name = 'employment_within_10_minutes_travel_time_hbw_am_drive_alone'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['employment_within_30_minutes_travel_time_hbw_am_drive_alone'], 
    computed_indicators = computed_indicators,
    visualization_type = 'mapnik_map',
    #name = 'employment_within_30_minutes_travel_time_hbw_am_drive_alone'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['travel_time_to_611'], 
    computed_indicators = computed_indicators,
    visualization_type = 'mapnik_map',
    #name = 'travel_time_to_611'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['travel_time_accessibility'], 
    computed_indicators = computed_indicators,
    visualization_type = 'mapnik_map',
    #name = 'travel_time_accessibility'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['improvement_value'], 
    computed_indicators = computed_indicators,
    visualization_type = 'mapnik_map',
    #name = 'number_of_households'
    )

### these are tables

visualizations += visualizer.visualize(
    indicators_to_visualize = ['population'],
    computed_indicators = computed_indicators,
    visualization_type = 'table',
    output_type = 'csv',
    #name = 'population',
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['income_per_person'],
    computed_indicators = computed_indicators,
    visualization_type = 'table',
    output_type = 'csv',
    #name = 'population'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['residential_units'], 
    computed_indicators = computed_indicators,
    visualization_type = 'table',
    output_type = 'csv',
    #name = 'residential_units'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['price_per_residential_unit'], 
    computed_indicators = computed_indicators,
    visualization_type = 'table',
    output_type = 'csv',
    #name = 'price_per_residential_unit'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['price_per_residential_sqft'], 
    computed_indicators = computed_indicators,
    visualization_type = 'table',
    output_type = 'csv',
    #name = 'price_per_residential_unit'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['parcel_price_per_residential_unit'], 
    computed_indicators = computed_indicators,
    visualization_type = 'table',
    output_type = 'csv',
    #name = 'price_per_residential_unit'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['parcel_price_per_residential_sqft'], 
    computed_indicators = computed_indicators,
    visualization_type = 'table',
    output_type = 'csv',
    #name = 'price_per_residential_unit'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['admin_sqft'], 
    computed_indicators = computed_indicators,
    visualization_type = 'table',
    output_type = 'csv',
    #name = 'admin_sqft'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['green_areas_sqft'], 
    computed_indicators = computed_indicators,
    visualization_type = 'table',
    output_type = 'csv',
    #name = 'admin_sqft'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['transport_sqft'], 
    computed_indicators = computed_indicators,
    visualization_type = 'table',
    output_type = 'csv',
    #name = 'admin_sqft'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['commerce_sqft'], 
    computed_indicators = computed_indicators,
    visualization_type = 'table',
    output_type = 'csv',
    #name = 'admin_sqft'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['industry_sqft'], 
    computed_indicators = computed_indicators,
    visualization_type = 'table',
    output_type = 'csv',
    #name = 'admin_sqft'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['gastronomy_sqft'], 
    computed_indicators = computed_indicators,
    visualization_type = 'table',
    output_type = 'csv',
    #name = 'admin_sqft'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['out_building_sqft'], 
    computed_indicators = computed_indicators,
    visualization_type = 'table',
    output_type = 'csv',
    #name = 'admin_sqft'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['number_of_jobs'],
    computed_indicators = computed_indicators,
    visualization_type = 'table',
    output_type = 'csv',
    #name = 'number_of_jobs',
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['number_of_households'], 
    computed_indicators = computed_indicators,
    visualization_type = 'table',
    output_type = 'csv',
    #name = 'number_of_households'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['average_household_income'],
    computed_indicators = computed_indicators,
    visualization_type = 'table',
    output_type = 'csv',
    #name = 'average_income'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['used_land_area'],
    computed_indicators = computed_indicators,
    visualization_type = 'table',
    output_type = 'csv',
    #name = 'average_income'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['vacant_land_area'],
    computed_indicators = computed_indicators,
    visualization_type = 'table',
    output_type = 'csv',
    #name = 'average_income'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['demolition_cost'],
    computed_indicators = computed_indicators,
    visualization_type = 'table',
    output_type = 'csv',
    #name = 'average_income'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['employment_within_10_minutes_travel_time_hbw_am_drive_alone'], 
    computed_indicators = computed_indicators,
    visualization_type = 'table',
    output_type = 'csv',
    #name = 'employment_within_10_minutes_travel_time_hbw_am_drive_alone'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['employment_within_30_minutes_travel_time_hbw_am_drive_alone'], 
    computed_indicators = computed_indicators,
    visualization_type = 'table',
    output_type = 'csv',
    #name = 'employment_within_10_minutes_travel_time_hbw_am_drive_alone'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['travel_time_to_611'], 
    computed_indicators = computed_indicators,
    visualization_type = 'table',
    output_type = 'csv',
    #name = 'travel_time_to_611'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['travel_time_accessibility'], 
    computed_indicators = computed_indicators,
    visualization_type = 'table',
    output_type = 'csv',
    #name = 'travel_time_accessibility'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['improvement_value'], 
    computed_indicators = computed_indicators,
    visualization_type = 'table',
    output_type = 'csv',
    #name = 'improvement_value'
    )

print 'Finished with creating indicators'