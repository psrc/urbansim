# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

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


#some cache_directories and run descriptions
#cache_directory = r'Y:/urbansim_cache/run_1090.2006_11_14_12_12'
#run_description = '(run 1090 - double highway capacity 11/28/2006)'
#cache_directory = r'Y:/urbansim_cache/run_1091.2006_11_14_12_12'
#run_description = '(run 1091 - baseline 11/28/2006)'
#cache_directory = r'D:\urbansim_cache\run_1454.2006_12_12_16_28'
#run_description = '(run 1454 - travel data from quick travel model)'
#cache_directory = r'D:\urbansim_cache\run_1090.2006_11_14_12_12'
cache_directory = r'C:\cache\run_1090.2006_11_14_12_12'
run_description = '(run 1453 - travel data from full travel model)'
#cache_directory = r'Y:\urbansim_cache\run_1431.2006_12_08_09_45'
#run_description = '(run 1431 - baseyear travel data from travel model run)'
#cache_directory = r'D:\urbansim_cache\run_1154.2006_11_17_20_06'
#run_description = '(run 1154 - no ugb + double highway capacity 11/28/2006)'
#cache_directory = r'D:\urbansim_cache\run_1155.2006_11_17_20_07'
#run_description = '(run 1155 - no ugb 11/28/2006)'

source_data = SourceData(
    cache_directory = cache_directory,
    run_description = run_description,
    years = [2000],
    dataset_pool_configuration = DatasetPoolConfiguration(
        package_order=['psrc','urbansim','opus_core'],
        ),       
)
single_year_requests = [

   DatasetTable(
       years = [2000],
       source_data = source_data,
       dataset_name = 'zone',
       name = 'pop_and_ind_sqft',
       attributes = [ 
         'urbansim.zone.population',
         'urbansim.zone.industrial_sqft',                     
       ],
       #exclude_condition = '==0' #exclude_condition now accepts opus expressions
   ),
   
    Map(
        attribute = 'psrc.large_area.population',
        scale = [1, 750000],
        dataset_name = 'large_area',
        source_data = source_data,
        ),
    Map(
        attribute = 'psrc.large_area.number_of_jobs_without_resource_construction_sectors',
        scale = [1, 700000],
        dataset_name = 'large_area',
        source_data = source_data,
        ),
    GeotiffMap(
        attribute = 'urbansim.gridcell.population',
        dataset_name = 'gridcell',
        package = 'psrc', 
        source_data = source_data,
        ),
    Map(
        attribute = 'psrc.large_area.de_employment_DDDD',
        scale = [1, 700000],
        dataset_name = 'large_area',
        source_data = source_data,
        ),
    Map(
        attribute = 'psrc.large_area.share_of_population',
        scale = [0.0, 0.2],
        dataset_name = 'large_area',
        source_data = source_data,
        ),
    Map(
        attribute = 'psrc.large_area.share_of_employment',
        scale = [0, 0.2],
        dataset_name = 'large_area',
        source_data = source_data,
        ),
    Map(
        attribute = 'psrc.large_area.share_of_de_population_DDDD',
        scale = [0, 0.2],
        dataset_name = 'large_area',
        source_data = source_data,
        ),
    Map(
        attribute = 'psrc.large_area.share_of_de_employment_DDDD',
        scale = [0, 0.2],
        dataset_name = 'large_area',
        source_data = source_data,
        ),
    Map(
        scale = [-5000, 250000],
        name = 'urbansim_population_change',
        attribute = 'psrc.large_area.population',
        source_data = source_data,
        operation = 'change',
        dataset_name = 'large_area',
        ),
    Table(
       source_data = source_data,
       dataset_name = 'large_area',
       name = 'test_overwrite',
       #operation = 'change',
       attribute = 'large_area.aggregate(urbansim.zone.number_of_jobs, intermediates=[faz])',
       years = [2000, 2005]
    ), 
    Table(
       source_data = source_data,
       dataset_name = 'large_area',
       name = 'test_overwrite2',
       #operation = 'change',
       attribute = 'large_area.aggregate(urbansim.zone.number_of_jobs, intermediates=[faz])',
       years = [2000, 2005]
    ), 
    
    Table(
       source_data = source_data,
       dataset_name = 'zone',
       name = 'test_overwrite3',
       operation = 'change',
       attribute = 'urbansim.zone.number_of_jobs',
       years = [2000, 2005]
    ), 
    Table(
       source_data = source_data,
       dataset_name = 'zone',
       name = 'test_overwrite4',
       operation = 'change',
       attribute = 'urbansim.zone.number_of_jobs',
       years = [2000]
    ), 
    Map(
        scale = [1000, 200000],
        name = 'urbansim_employment_change',
        attribute = 'psrc.large_area.number_of_jobs_without_resource_construction_sectors',
        operation = 'change',
        source_data = source_data,
        dataset_name = 'large_area',
        ),
    Map(
        scale = [-5000, 250000],
        name = 'de_population_change',
        source_data = source_data,
        attribute = 'psrc.large_area.de_population_DDDD',
        operation = 'change',
        dataset_name = 'large_area',
        ),
    Map(
        scale = [1000, 200000],
        name = 'de_employment_change',
        attribute = 'psrc.large_area.de_employment_DDDD',
        operation = 'change',
        source_data = source_data,
        dataset_name = 'large_area',
        ),
    Map(
        scale = [-0.02, 0.02],
        name = 'share_of_de_population_change',
        source_data = source_data,
        attribute = 'psrc.large_area.share_of_de_population_DDDD',
        operation = 'change',
        dataset_name = 'large_area',
        ),
    Map(
        scale = [-0.03, 0.03],
        name = 'share_of_de_employment_change',
        source_data = source_data,
        attribute = 'psrc.large_area.share_of_de_employment_DDDD',
        operation = 'change',
        dataset_name = 'large_area',
        ),
    Map(
        scale = [-75000, 100000],
        name = 'urbansim_de_population_difference',
        attribute = 'psrc.large_area.population-psrc.large_area.de_population_DDDD',
        source_data = source_data,
        dataset_name = 'large_area',
        ),
    Map(
        scale = [-50000, 25000],
        name = 'urbansim_de_employment_difference',
        attribute = 'psrc.large_area.number_of_jobs_without_resource_construction_sectors-psrc.large_area.de_employment_DDDD',
        source_data = source_data,
        dataset_name = 'large_area',
        ),
    Map(
        scale = [-0.03, 0.03],
        name = 'urbansim_de_share_of_population_difference',
        attribute = 'psrc.large_area.share_of_population-psrc.large_area.share_of_de_population_DDDD',
        source_data = source_data,
        dataset_name = 'large_area',
        ),
    Map(
        scale = [-0.02, 0.02],
        name = 'urbansim_de_share_of_employment_difference',
        source_data = source_data,
        attribute = 'psrc.large_area.share_of_employment-psrc.large_area.share_of_de_employment_DDDD',
        dataset_name = 'large_area',
        ),
    Map(
        attribute = 'urbansim.faz.population',
        scale = [1, 60000],
        dataset_name = 'faz',
        source_data = source_data,
        ),
    Table(
        attribute = 'urbansim.faz.population',
        dataset_name = 'faz',
        source_data = source_data,
        ),
    Table(
        attribute = 'de_population_DDDD',
        dataset_name = 'faz',
        source_data = source_data,
        ),
    Map(
        attribute = 'psrc.faz.number_of_jobs_without_resource_construction_sectors',
        scale = [1, 60000],
        dataset_name = 'faz',
        source_data = source_data,
        ),
    Map(
        attribute = 'psrc.faz.share_of_population',
        scale = [0.0, 0.02],
        dataset_name = 'faz',
        source_data = source_data,
        ),
    Map(
        attribute = 'psrc.faz.share_of_employment',
        scale = [0, 0.1],
        dataset_name = 'faz',
        source_data = source_data,
        ),
    Map(
        attribute = 'psrc.faz.share_of_de_population_DDDD',
        scale = [0, 0.02],
        dataset_name = 'faz',
        source_data = source_data,
        ),
    Map(
        attribute = 'psrc.faz.share_of_de_employment_DDDD',
        scale = [0, 0.1],
        dataset_name = 'faz',
        source_data = source_data,
        ),
    Map(
        attribute = 'de_population_DDDD',
        scale = [1, 60000],
        dataset_name = 'faz',
        source_data = source_data,
        ),
    Map(
        attribute = 'de_employment_DDDD',
        scale = [1, 150000],
        dataset_name = 'faz',
        source_data = source_data,
        ),
    Map(
        scale = [-8000, 40000],
        name = 'urbansim_population_change',
        source_data = source_data,
        attribute = 'urbansim.faz.population',
        operation = 'change',
        dataset_name = 'faz',
        ),
    Map(
        scale = [-2000, 40000],
        name = 'urbansim_employment_change',
        source_data = source_data,
        operation = 'change',
        attribute = 'psrc.faz.number_of_jobs_without_resource_construction_sectors',
        dataset_name = 'faz',
        ),

    Map(
        attribute = 'psrc.zone.generalized_cost_hbw_am_drive_alone_to_129',
        scale = [-10, 140],
        dataset_name = 'zone',
        source_data = source_data,
        ),
    Map(
        attribute = 'psrc.zone.travel_time_hbw_am_drive_alone_to_cbd',
        scale = [-10, 110],
        dataset_name = 'zone',
        source_data = source_data,
        ),
    Map(
        attribute = 'psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone',
        scale = [-1000, 8000],
        dataset_name = 'zone',
        source_data = source_data,
        ),
    Map(
        attribute = 'psrc.zone.travel_time_weighted_access_to_employment_hbw_am_drive_alone',
        scale = [-1000, 7000],
        dataset_name = 'zone',
        source_data = source_data,
        ),
    Map(
        attribute = 'urbansim.zone.number_of_jobs',
        scale = [1, 60000],
        dataset_name = 'zone',
        source_data = source_data,
        ),
    Map(
        attribute = 'psrc.zone.number_of_jobs_per_acre',
        scale = [1, 1000],
        dataset_name = 'zone',
        source_data = source_data,
        ),
    ]

source_data = SourceData(
    cache_directory = cache_directory,
    run_description = run_description,
    years = [2000],
    dataset_pool_configuration = DatasetPoolConfiguration(
        package_order=['psrc','urbansim','opus_core'],
        ),       
)

multi_year_requests = [
    Table(
        attribute = 'alldata.aggregate_all(urbansim.gridcell.residential_units, function=sum)',
        dataset_name = 'alldata',
        source_data = source_data,
        name = 'Residential_Units'
        ),
    Chart(
        attribute = 'psrc.county.population',
        dataset_name = 'county',
        source_data = source_data,
        ),
    Chart(
        attribute = 'psrc.county.number_of_jobs',
        dataset_name = 'county',
        source_data = source_data,
        ),
    Table(
        attribute = 'psrc.large_area.population',
        dataset_name = 'large_area',
        source_data = source_data,
        ),
    Table(
        attribute = 'psrc.large_area.number_of_jobs_without_resource_construction_sectors',
        dataset_name = 'large_area',
        source_data = source_data,
        ),
    Table(
        attribute = 'psrc.large_area.average_land_value_for_plan_type_group_residential',
        dataset_name = 'large_area',
        source_data = source_data,
        ),
    Table(
        attribute = 'psrc.large_area.average_land_value_for_plan_type_group_non_residential',
        dataset_name = 'large_area',
        source_data = source_data,
        ),
    Table(
        attribute = 'psrc.large_area.population',
        dataset_name = 'large_area',
        source_data = source_data,
        ),
    Table(
        attribute = 'psrc.large_area.number_of_jobs',
        dataset_name = 'large_area',
        source_data = source_data,
        ),
    Table(
        attribute = 'psrc.county.population',
        dataset_name = 'county',
        source_data = source_data,
        ),
    Table(
        attribute = 'psrc.county.number_of_jobs',
        dataset_name = 'county',
        source_data = source_data,
        ),

    Table(
        attribute = 'psrc.zone.generalized_cost_hbw_am_drive_alone_to_129',
        dataset_name = 'zone',
        source_data = source_data,
        ),
    Table(
        attribute = 'psrc.zone.travel_time_hbw_am_drive_alone_to_cbd',
        dataset_name = 'zone',
        source_data = source_data,
        ),
    Table(
        attribute = 'psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone',
        dataset_name = 'zone',
        source_data = source_data,
        ),
    Table(
        attribute = 'psrc.zone.travel_time_weighted_access_to_employment_hbw_am_drive_alone',
        dataset_name = 'zone',
        source_data = source_data,
        ),
    Table(
        attribute = 'urbansim.zone.number_of_jobs',
        dataset_name = 'zone',
        source_data = source_data,
        ),
    Table(
        attribute = 'alldata.aggregate_all(urbansim.zone.number_of_home_based_jobs)',
        dataset_name = 'alldata',
        source_data = source_data,
        name =  'number_of_home_based_jobs'
        ),

    ]

if __name__ == '__main__':
    from opus_core.indicator_framework.core.indicator_factory import IndicatorFactory

    IndicatorFactory().create_indicators(
        indicators = single_year_requests,
        display_error_box = False, 
        show_results = True)   
#    IndicatorFactory().create_indicators(
#        indicators = multi_year_requests,
#        display_error_box = False, 
#        show_results = True)   