# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

# script to produce a number of indicators

from inprocess.travis.urbansim.indicator_framework.source_data import SourceData
from inprocess.travis.urbansim.indicator_framework.image_types.matplotlib_map import Map
from inprocess.travis.urbansim.indicator_framework.image_types.matplotlib_chart import Chart
from inprocess.travis.urbansim.indicator_framework.image_types.table import Table
from inprocess.travis.urbansim.indicator_framework.image_types.geotiff_map import GeotiffMap
from inprocess.travis.urbansim.indicator_framework.image_types.arcgeotiff_map import ArcGeotiffMap
from inprocess.travis.urbansim.indicator_framework.image_types.dataset_table import DatasetTable
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration

source_data = SourceData(
   cache_directory = r'D:\urbansim_cache\run_1090.2006_11_14_12_12',
   #for running a cross-scenario indicator comparison, set this field in the source_data:
   #(note that a subtract will be performed for equivalent values between scenarios)
#   cache_directory_2 = r'D:\urbansim_cache\run_1091.2006_11_14_12_12',
   #years is the default years that all the indicators will be computed for.
   #each indicator request can optionally have a 'years' key whose value is 
   #used instead of years for that particular indicator
   years = [2000, 2010, 2020, 2030],
   dataset_pool_configuration = DatasetPoolConfiguration(
                package_order=['psrc', 'urbansim', 'opus_core'])
)
#
# When the attribute name includes the year as "DDDD", it will be replaced
# each year the indicator is computed for.

indicators = [
   Map( #every indicator output type takes dataset, attribute, and (optionally) years
       source_data = source_data,
       dataset_name = 'zone',
       attribute = 'psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone as E20MDA',
       years = [2001, 2006, 2011, 2016, 2021, 2026], #optional years field; if not specified, defaults to source_data.years
       ),  
   
#   Chart(
#       source_data = source_data,
#       dataset_name = 'gridcell',
#       attribute = 'urbansim.gridcell.population',
#       ),  
   
   Table(
       source_data = source_data,
       dataset_name = 'zone',
       attribute = 'LNE40MTW = ln_bounded(psrc.zone.employment_within_40_minutes_travel_time_hbw_am_transit_walk)',
       output_type = 'tab', #can also be 'csv'
       years = [2001, 2006, 2011, 2016, 2021, 2026]
       ),  
       
#   GeotiffMap(
#       source_data = source_data,
#       dataset_name = 'gridcell',
#       attribute = 'urbansim.gridcell.number_of_jobs', 
#       name = 'jobs', #optional parameter that replaces the 'as'. Defaults to attribute name; in this case, 'number_of_jobs'
#       #prototype_dataset = 'blah', #(this argument defaults to the path to inprocess.travis.psrc.images.idgrid.tif)
#    ),
    
   DatasetTable(
       source_data = source_data,
       dataset_name = 'large_area',
       name = 'population_and_employment', #optional parameter which replaces the 'as' syntax
       attributes = [ #list of attributes that will be columns in the resulting table
         'psrc.large_area.population',
         'psrc.large_area.number_of_jobs_without_resource_construction_sectors',
       ],
       condition = '==0' #an optional filter for when rows are not included in the result            
   ),

#   ArcGeotiffMap(
#       source_data = source_data,
#       dataset_name = 'gridcell',
#       attribute = 'urbansim.gridcell.number_of_jobs', 
#       #prototype_dataset = 'blah', (this argument defaults to the path to inprocess.travis.psrc.images.idgrid.tif
#       layer_file = 'D:/ArcMap_automation/6_RedClassBreaks_noZeroValues.lyr', #(optional); will default to ''
#       transparency = 0, #(optional); will default to 0
#       exit_after_export = True, #(optional) Should arcmap exit when its done exporting the indicator? Will default to False
#       export_type = 'jpg', #(optional) Output format for arcmap; will default to jpg
#    ),

   Map(
       source_data = source_data,
       dataset_name = 'faz',
       name = 'population_change(DDDD-00)',
       expression = {
         'operation':'change',
         'operands': ['urbansim.faz.population']
         },
       scale = [-5000, 250000],
       years = [2030]
   ),

   Map(
       source_data = source_data,
       dataset_name = 'faz',
       name = 'employment_change(DDDD-00)',
       expression = {
         'operation':'change',
         'operands': ['psrc.faz.number_of_jobs_without_resource_construction_sectors']
         },
       scale = [-5000, 250000],
       years = [2030]
   ),   
]

if __name__ == '__main__':
    from inprocess.travis.urbansim.indicator_framework.indicator_factory import IndicatorFactory

    IndicatorFactory().create_indicators(
        indicators = indicators,
        display_error_box = False, 
        show_results = True)    