# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

# script to produce a number of PSRC indicators -- 
# this illustrates using traits-based configurations programatically


from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.indicator_framework.core.source_data import SourceData

from opus_core.indicator_framework.image_types.matplotlib_map import Map
from opus_core.indicator_framework.image_types.matplotlib_chart import Chart
from opus_core.indicator_framework.image_types.table import Table
from opus_core.indicator_framework.image_types.geotiff_map import GeotiffMap
from opus_core.indicator_framework.image_types.dataset_table import DatasetTable
from opus_core.indicator_framework.image_types.matplotlib_lorenzcurve import LorenzCurve
from opus_core.database_management.configurations.database_configuration import DatabaseConfiguration


run_description = '(baseline 11/26/2007)'
cache_directory = r'/urbansim_cache/psrc_parcel/run_5900.2008_04_02_12_40'

#run_description = '(no build 11/26/2007)'
#cache_directory = r'D:\urbansim_cache\run_4169.2007_11_21_00_12'

source_data = SourceData(
    cache_directory = cache_directory,
    run_description = run_description,
    years = [2002],  #range(2000, 2021, 10),
    dataset_pool_configuration = DatasetPoolConfiguration(
        package_order=['psrc_parcel','urbansim_parcel','psrc', 'urbansim','opus_core'],
        ),       
)

indicators=[
#    Table(
#        attribute = 'population=large_area.aggregate(urbansim_parcel.building.population, intermediates=[parcel, zone, faz])',
#        dataset_name = 'large_area',
#        source_data = source_data,
#        ),
#    Table(
#        attribute = 'employment=large_area.aggregate(urbansim_parcel.building.number_of_jobs, intermediates=[parcel, zone, faz])',
#        dataset_name = 'large_area',
#        source_data = source_data,
#        ),
    Table(
        attribute = 'at_home_workers=district.aggregate(person.work_at_home==1, intermediates=[household, building, parcel, zone])',
        dataset_name = 'district',
        source_data = source_data,
        ),
    DatasetTable(
        attributes = [
            'origin_district_id',
            'destination_district_id',
            'psrc_parcel.district_commute.commute_trips',
            ],
        dataset_name = 'district_commute',
        source_data = source_data,
        name = 'commutes_by_district',
        ),
#    Map(
#        attribute = 'population=zone.aggregate(urbansim_parcel.building.population, intermediates=[parcel])',
#        dataset_name = 'zone',
#        source_data = source_data,
#        ),
#    Map(
#        attribute = 'faz_employment=faz.aggregate(urbansim_parcel.building.number_of_jobs, intermediates=[parcel,zone])',
#        dataset_name = 'faz',
#        source_data = source_data,
#        ),
#    Map(
#        name = 'population_change',
#        source_data = source_data,
#        attribute = 'population=faz.aggregate(urbansim_parcel.building.population, intermediates=[parcel,zone])',
#        operation = 'change',
#        dataset_name = 'faz',
#        ),
#    DatasetTable(
#        source_data = source_data,
#        dataset_name = 'building',
#        name =  'new_bldg',
#        attributes = [
#            'building.building_id',
#            'urbansim_parcel.building.unit_price',
#            'urbansim_parcel.building.residential_units',
#            'urbansim_parcel.building.vacant_residential_units',
#            'urbansim_parcel.building.year_built',
#        ],
#        exclude_condition = 'building.year_built<DDDD',
#    ),

]
from opus_core.indicator_framework.core.indicator_factory import IndicatorFactory

IndicatorFactory().create_indicators(
     indicators = indicators,
     display_error_box = False, 
     show_results = True)    
