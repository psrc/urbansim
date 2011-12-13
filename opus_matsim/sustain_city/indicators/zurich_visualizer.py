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

# zurich scenario from 2000 to 2010
cache_directory = r'/Users/sustaincity/Development/opus_home/data/zurich_parcel_from_20111014/runs/run_4.test_no_action_10pct_30it_2000-2010'

types = ['mapnik_map']

print "creating indicators for %s" % os.environ['OPUSPROJECTNAME']

indicators = {
    
    'population':Indicator(
        dataset_name = 'zone',
        attribute = 'urbansim_parcel.zone.population_per_acre' ),
              
    # No further division into single family or multi family residential!  (Wohngebaeude)
    'residential_units':Indicator(
        dataset_name = 'zone',
        attribute = 'zone.aggregate(building.residential_units * (building.building_type_id==1))' ),
    'residential_unit_price':Indicator(
        dataset_name = 'zone',
        attribute = 'zone.aggregate(building.average_value_per_unit * building.residential_units * (building.building_type_id==1))' ),          
     
     # Verwaltung
     'amin_sqft':Indicator(
        dataset_name = 'zone',
        attribute = 'zone.aggregate(building.non_residential_sqft * (building.building_type_id==0))' ),
    'amin_sqft':Indicator(
        dataset_name = 'zone',
        attribute = 'zone.aggregate(building.non_residential_sqft * (building.building_type_id==0))' ),
           
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
         package_order=['zurich_parcel','urbansim_parcel', 'urbansim', 'psrc', 'opus_core'],
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
    indicators_to_visualize = ['population'], #override default indicators to visualize (all)
    computed_indicators = computed_indicators,
    visualization_type = 'mapnik_map',
    name = 'population'
    )


print 'Finished with creating indicators'