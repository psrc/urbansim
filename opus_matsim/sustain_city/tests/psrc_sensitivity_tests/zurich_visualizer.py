# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE


#############################################################
#DEFINE indicators
#############################################################
import os
from opus_gui.results_manager.run.indicator_framework.representations.indicator import Indicator

project_name = pn = 'zurich_parcel' #'seattle_parcel'
# setting project name to environment. this is needed for the visualizer
os.environ['OPUSPROJECTNAME'] = pn

years_arr = [2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010]

# cupum scenarios 2030 re-estimated
cache_dir = r'/Users/sustaincity/Development/opus_home/data/zurich_parcel_from_20111014/runs/run_4.test_no_action_10pct_30it_2000-2010' #'/Users/sustaincity/Development/opus_home/data/seattle_parcel/base_year_data' # highway limited cap.

types = ['mapnik_map']

print "creating indicators for %s" % os.environ['OPUSPROJECTNAME']

indicators = {
    
    'population':Indicator(
        dataset_name = 'zone',
        attribute = 'urbansim_parcel.zone.population_per_acre' ),
              
    


    ### koennen aussortiert werden:
    
    'residential_sqft_per_unit2':Indicator(
       dataset_name = 'zone',
       attribute = 'zone.aggregate(safe_array_divide(urbansim_parcel.building.building_sqft * urbansim_parcel.building.is_residential,building.residential_units), intermediates=[parcel])'),
    
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
from opus_core.database_management.configurations.database_configuration import DatabaseConfiguration

visualizer = VisualizationFactory()
visualizations = []

# View an indicator as a Map
visualizations += visualizer.visualize(
    indicators_to_visualize = ['population'], #override default indicators to visualize (all)
    computed_indicators = computed_indicators,
    visualization_type = 'mapnik_map',
    name = 'population'
    )

visualizations += visualizer.visualize(
    indicators_to_visualize = ['residential_sqft_per_unit2'],
    computed_indicators = computed_indicators,
    visualization_type = 'mapnik_map',
    name = 'residential_sqft_per_unit2',
    )

print 'Finished with creating indicators'