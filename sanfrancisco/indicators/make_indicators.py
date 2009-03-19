# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

# script to produce a number of PSRC indicators -- 
# this illustrates using traits-based configurations programatically

from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.indicator_framework.core.source_data import SourceData
from numpy import arange
from opus_core.indicator_framework.image_types.matplotlib_map import Map
from opus_core.indicator_framework.image_types.matplotlib_chart import Chart
from opus_core.indicator_framework.image_types.table import Table
from opus_core.indicator_framework.image_types.geotiff_map import GeotiffMap
from opus_core.indicator_framework.image_types.dataset_table import DatasetTable
from opus_core.indicator_framework.image_types.matplotlib_lorenzcurve import LorenzCurve


run_description = '(baseline 06/28/2007)'
cache_directory = r'/Volumes/Data/opus/data/sanfrancisco/runs/run_2.2008_12_30_13_34'

source_data = SourceData(
    cache_directory = cache_directory,
    run_description = run_description,
    years = [2001, 2002, 2005, 2007, 2010, 2020, 2030],
    dataset_pool_configuration = DatasetPoolConfiguration(
        package_order=['sanfrancisco','urbansim','opus_core'],
        ),       
)
single_year_requests = [

       DatasetTable(
       source_data = source_data,
       dataset_name = 'census_tract',
       name = 'Tract Indicators',
       output_type='csv',
       attributes = [ 
                     'households_with_0_workers=census_tract.aggregate(sanfrancisco.building.number_of_households_with_0_workers, intermediates=[parcel])',
                     'households_with_1_worker =census_tract.aggregate(sanfrancisco.building.number_of_households_with_1_workers, intermediates=[parcel])',
                     'households_with_2_workers=census_tract.aggregate(sanfrancisco.building.number_of_households_with_2_workers, intermediates=[parcel])',
                     'households_with_3_workers=census_tract.aggregate(sanfrancisco.building.number_of_households_with_3_workers, intermediates=[parcel])',
                     'households_with_4_workers=census_tract.aggregate(sanfrancisco.building.number_of_households_with_4_workers, intermediates=[parcel])',
                     'households_with_5_workers=census_tract.aggregate(sanfrancisco.building.number_of_households_with_5_workers, intermediates=[parcel])',
                     'households_with_6_workers=census_tract.aggregate(sanfrancisco.building.number_of_households_with_6_workers, intermediates=[parcel])',
                     'households_with_7_workers=census_tract.aggregate(sanfrancisco.building.number_of_households_with_7_workers, intermediates=[parcel])',
                     'total_households=census_tract.aggregate(sanfrancisco.building.number_of_households, intermediates=[parcel])',
                     'total_population=census_tract.aggregate(sanfrancisco.building.population, intermediates=[parcel])',                                     
                     'sector_1_employment=census_tract.aggregate(sanfrancisco.building.employment_of_sector_1, intermediates=[parcel])',
                     'sector_2_employment=census_tract.aggregate(sanfrancisco.building.employment_of_sector_2, intermediates=[parcel])',
                     'sector_3_employment=census_tract.aggregate(sanfrancisco.building.employment_of_sector_3, intermediates=[parcel])',
                     'sector_4_employment=census_tract.aggregate(sanfrancisco.building.employment_of_sector_4, intermediates=[parcel])',
                     'sector_5_employment=census_tract.aggregate(sanfrancisco.building.employment_of_sector_5, intermediates=[parcel])',
                     'sector_6_employment=census_tract.aggregate(sanfrancisco.building.employment_of_sector_6, intermediates=[parcel])',
                     'total_employment=census_tract.aggregate(sanfrancisco.building.employment, intermediates=[parcel])',
                     'sector_1_businesses=census_tract.aggregate(business.sector_id == 1, intermediates=[building, parcel])',
                     'sector_2_businesses=census_tract.aggregate(business.sector_id == 2, intermediates=[building, parcel])',
                     'sector_3_businesses=census_tract.aggregate(business.sector_id == 3, intermediates=[building, parcel])',
                     'sector_4_businesses=census_tract.aggregate(business.sector_id == 4, intermediates=[building, parcel])',
                     'sector_5_businesses=census_tract.aggregate(business.sector_id == 5, intermediates=[building, parcel])',
                     'sector_6_businesses=census_tract.aggregate(business.sector_id == 6, intermediates=[building, parcel])',
                     'total_businesses=census_tract.aggregate(sanfrancisco.building.number_of_businesses, intermediates=[parcel])',
       ],
       #exclude_condition = '==0' #exclude_condition now accepts opus expressions
       ),

       DatasetTable(
       source_data = source_data,
       dataset_name = 'zone',
       name = 'Zone Indicators',
       output_type='csv',
       attributes = [ 
                     'households_with_0_workers=zone.aggregate(sanfrancisco.building.number_of_households_with_0_workers, intermediates=[parcel])',
                     'households_with_1_worker =zone.aggregate(sanfrancisco.building.number_of_households_with_1_workers, intermediates=[parcel])',
                     'households_with_2_workers=zone.aggregate(sanfrancisco.building.number_of_households_with_2_workers, intermediates=[parcel])',
                     'households_with_3_workers=zone.aggregate(sanfrancisco.building.number_of_households_with_3_workers, intermediates=[parcel])',
                     'households_with_4_workers=zone.aggregate(sanfrancisco.building.number_of_households_with_4_workers, intermediates=[parcel])',
                     'households_with_5_workers=zone.aggregate(sanfrancisco.building.number_of_households_with_5_workers, intermediates=[parcel])',
                     'households_with_6_workers=zone.aggregate(sanfrancisco.building.number_of_households_with_6_workers, intermediates=[parcel])',
                     'households_with_7_workers=zone.aggregate(sanfrancisco.building.number_of_households_with_7_workers, intermediates=[parcel])',
                     'total_households=zone.aggregate(sanfrancisco.building.number_of_households, intermediates=[parcel])',
                     'total_population=zone.aggregate(sanfrancisco.building.population, intermediates=[parcel])',                                     
                     'sector_1_employment=zone.aggregate(sanfrancisco.building.employment_of_sector_1, intermediates=[parcel])',
                     'sector_2_employment=zone.aggregate(sanfrancisco.building.employment_of_sector_2, intermediates=[parcel])',
                     'sector_3_employment=zone.aggregate(sanfrancisco.building.employment_of_sector_3, intermediates=[parcel])',
                     'sector_4_employment=zone.aggregate(sanfrancisco.building.employment_of_sector_4, intermediates=[parcel])',
                     'sector_5_employment=zone.aggregate(sanfrancisco.building.employment_of_sector_5, intermediates=[parcel])',
                     'sector_6_employment=zone.aggregate(sanfrancisco.building.employment_of_sector_6, intermediates=[parcel])',
                     'total_employment=zone.aggregate(sanfrancisco.building.employment, intermediates=[parcel])',
       ],
       #exclude_condition = '==0' #exclude_condition now accepts opus expressions
),

    ]

source_data = SourceData(
    cache_directory = cache_directory,
    run_description = run_description,
    years = [2001,2002],
    dataset_pool_configuration = DatasetPoolConfiguration(
        package_order=['sanfrancisco','urbansim','opus_core'],
        ),       
)

multi_year_requests = [
    #Chart(
        #attribute = 'bus_ = alldata.aggregate_all(business.sector_id == 1)',
        #dataset_name = 'alldata',
        #source_data = source_data,
        #years=arange(2001,2026),
        #),
    
    Table(
    source_data = source_data,
    dataset_name = 'alldata',
    name = 'Business Counts 1',
    output_type='csv',
    attribute = 'bus_1 = alldata.aggregate_all(business.sector_id == 1)',
    years = [2001, 2002],
    ),
    
    Table(
    source_data = source_data,
    dataset_name = 'alldata',
    name = 'Business Counts 2',
    output_type='csv',
    attribute = 'bus_2 = alldata.aggregate_all(business.sector_id == 2)',
    years = [2001, 2002],
    ),

    Table(
    source_data = source_data,
    dataset_name = 'alldata',
    name = 'Business Counts 3',
    output_type='csv',
    attribute = 'bus_3 = alldata.aggregate_all(business.sector_id == 3)',
    years = [2001, 2002],
    ),

    Table(
    source_data = source_data,
    dataset_name = 'alldata',
    name = 'Business Counts 4',
    output_type='csv',
    attribute = 'bus_4 = alldata.aggregate_all(business.sector_id == 4)',
    years = [2001, 2002],
    ),

    Table(
    source_data = source_data,
    dataset_name = 'alldata',
    name = 'Business Counts 5',
    output_type='csv',
    attribute = 'bus_5 = alldata.aggregate_all(business.sector_id == 5)',
    years = [2001, 2002],
    ),

    Table(
    source_data = source_data,
    dataset_name = 'alldata',
    name = 'Business Counts 6',
    output_type='csv',
    attribute = 'bus_6 = alldata.aggregate_all(business.sector_id == 6)',
    years = [2001, 2002],
    ),
]

if __name__ == '__main__':
    from opus_core.indicator_framework.core.indicator_factory import IndicatorFactory

    IndicatorFactory().create_indicators(
        indicators = single_year_requests,
        display_error_box = False, 
        show_results = True)   
    #IndicatorFactory().create_indicators(
        #indicators = multi_year_requests,
        #display_error_box = False, 
        #show_results = True)   