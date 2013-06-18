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
years_arr = [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030]

# cupum scenarios 2030 re-estimated
cache_directory = r'/Users/thomas/Development/opus_home/data/psrc_parcel/runs/run_4.2011_05_13_13_53' # highway limited cap.
#cache_directory = r'/Users/thomas/Development/opus_home/data/psrc_parcel/runs/run_4.2011_05_13_13_52' # highway
#cache_directory = r'/Users/thomas/Development/opus_home/data/psrc_parcel/runs/run_4.2011_05_13_13_47' # ferry

types = ['tab']

print "creating indicators ..."

indicators = {

    #'zone__autogenvar1':Indicator(
    #   dataset_name = 'zone',
    #   attribute = 'zone.aggregate( (urbansim_parcel.building.vacant_residential_units * urbansim_parcel.building.is_generic_building_type_1)/(building.residential_units * urbansim_parcel.building.is_generic_building_type_1) )'),
              
              
    #'zone__autogenvar0':Indicator(
    #   dataset_name = 'zone',
    #   attribute = 'zone.aggregate(urbansim_parcel.development_project_proposal.expected_rate_of_return_on_investment, function=mean)'),
              
    'alldata__autogenvar2':Indicator(
       dataset_name = 'alldata',
       attribute = 'alldata.aggregate_all(urbansim_parcel.building.vacant_residential_units*urbansim_parcel.building.is_generic_building_type_1)/alldata.aggregate_all(building.residential_units*urbansim_parcel.building.is_generic_building_type_1)'),

    #'vacancy_rate_mfr_alldata':Indicator(
    #   dataset_name = 'alldata',
    #   attribute = 'alldata.aggregate_all(urbansim_parcel.building.vacant_residential_units * urbansim_parcel.building.is_generic_building_type_2) / alldata.aggregate_all(building.residential_units * urbansim_parcel.building.is_generic_building_type_2)'),

    # this gives the mean profit for each proposal aggregated on zone
    #'zone__autogenvar0':Indicator(
    #   dataset_name = 'zone',
    #   attribute = 'zone.aggregate(urbansim_parcel.development_project_proposal.profit,function=mean,intermediates=[parcel])'),
    
    # this gives the mean profit for each proposal aggregated on zone
    #'zone__autogenvar1':Indicator(
    #   dataset_name = 'zone',
    #   attribute = 'zone.aggregate(urbansim_parcel.development_project_proposal.total_revenue,function=mean,intermediates=[parcel])'),
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

#try: # tnicolai :for debugging
#    import pydevd
#    pydevd.settrace()
#except: pass

for output_type in types:
    visualizations += visualizer.visualize(
        indicators_to_visualize = ['alldata__autogenvar2'],
        computed_indicators = computed_indicators,
        visualization_type = 'table',
        output_type = output_type,
        name = 'alldata__autogenvar2',
        )

#for output_type in types:
#    visualizations += visualizer.visualize(
#        indicators_to_visualize = ['zone__autogenvar1'],
#        computed_indicators = computed_indicators,
#        visualization_type = 'table',
#        output_type = output_type,
#        name = 'zone__autogenvar1',
#        )

#for output_type in types:
#    visualizations += visualizer.visualize(
#        indicators_to_visualize = ['vacancy_rate_mfr_alldata'],
#        computed_indicators = computed_indicators,
#        visualization_type = 'table',
#        output_type = output_type,
#        name = 'vacancy_rate_mfr_alldata',
#        )

end_time = time.time()

print "Computation took : %f\n" %(end_time-start_time)
print "Finished!!!"
