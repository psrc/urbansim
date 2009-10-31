# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

# script to produce a number of indicators

from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.indicator_framework.core.source_data import SourceData
from opus_core.indicator_framework.image_types.matplotlib_map import Map
from opus_core.indicator_framework.image_types.matplotlib_chart import Chart
from opus_core.indicator_framework.image_types.table import Table
from opus_core.indicator_framework.image_types.geotiff_map import GeotiffMap
from opus_core.indicator_framework.image_types.dataset_table import DatasetTable
from opus_core.indicator_framework.image_types.matplotlib_lorenzcurve import LorenzCurve
from opus_core.database_management.configurations.database_configuration import DatabaseConfiguration

source_data = SourceData(
   #cache_directory = r'D:\urbansim_cache\run_1090.2006_11_14_12_12',
   cache_directory = r'C:\urbansim_cache\psrc_zone\base_year_data',
   #comparison_cache_directory = r'D:\urbansim_cache\run_1091.2006_11_14_12_12',
   years = [2000],
   dataset_pool_configuration = DatasetPoolConfiguration(
         package_order=['urbansim_zone', 'urbansim_parcel', 'urbansim','opus_core'],
         ),                  
)

indicators = [
   DatasetTable(
       #years = [2000],
       source_data = source_data,
       dataset_name = 'zone',
       name = 'zone_indicators',
       attributes = [
         'sf_units = zone.aggregate(building.residential_units * (building.building_type_id==1))',
         'mf_units = zone.aggregate(building.residential_units * (building.building_type_id==2))',
         'off_sqft = zone.aggregate(building.non_residential_sqft * (building.building_type_id==3))',
         'com_sqft = zone.aggregate(building.non_residential_sqft * (building.building_type_id==4))',
         'ind_sqft = zone.aggregate(building.non_residential_sqft * (building.building_type_id==5))',
         
         'sf_unit_price = zone.aggregate(building.average_value_per_unit * building.sqft_per_unit * (building.building_type_id==1))',
         'mf_unit_price = zone.aggregate(building.average_value_per_unit * building.sqft_per_unit * (building.building_type_id==2))',
         'off_unit_price = zone.aggregate(building.non_residential_sqft * (building.building_type_id==3))',
         'com_unit_price = zone.aggregate(building.non_residential_sqft * (building.building_type_id==4))',
         'ind_unit_price = zone.aggregate(building.non_residential_sqft * (building.building_type_id==5))',
         
         'sf_capacity = zone.aggregate(building.residential_units_capacity * (building.building_type_id==1))',
         'mf_capacity = zone.aggregate(building.residential_units_capacity * (building.building_type_id==2))',
         'off_capacity = zone.aggregate(building.non_residential_sqft_capacity * (building.building_type_id==3))',
         'com_capacity = zone.aggregate(building.non_residential_sqft_capacity * (building.building_type_id==4))',
         'ind_capacity = zone.aggregate(building.non_residential_sqft_capacity * (building.building_type_id==5))',

         'dev_sf_capacity = zone.aggregate(building.residential_units_capacity * (building.building_type_id==1)) - zone.aggregate(building.residential_units * (building.building_type_id==1))',
         'dev_mf_capacity = zone.aggregate(building.residential_units_capacity * (building.building_type_id==2)) - zone.aggregate(building.residential_units * (building.building_type_id==2))',
         'dev_off_capacity = zone.aggregate(building.non_residential_sqft_capacity * (building.building_type_id==3)) - zone.aggregate(building.non_residential_sqft * (building.building_type_id==3))',
         'dev_com_capacity = zone.aggregate(building.non_residential_sqft_capacity * (building.building_type_id==4)) - zone.aggregate(building.non_residential_sqft * (building.building_type_id==4))',
         'dev_ind_capacity = zone.aggregate(building.non_residential_sqft_capacity * (building.building_type_id==5)) - zone.aggregate(building.non_residential_sqft * (building.building_type_id==5))',
         
       ],
       #exclude_condition = '==0' #exclude_condition now accepts opus expressions
   ),
   ]


if __name__ == '__main__':
    from opus_core.indicator_framework.core.indicator_factory import IndicatorFactory

    IndicatorFactory().create_indicators(
        indicators = indicators,
        display_error_box = False, 
        show_results = True)    