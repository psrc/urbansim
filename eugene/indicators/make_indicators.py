#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

# script to produce a number of PSRC indicators -- 
# this illustrates using traits-based configurations programatically

from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.indicator_framework.core import SourceData
from opus_core.indicator_framework.image_types import Map
from opus_core.indicator_framework.image_types import Chart
from opus_core.indicator_framework.image_types import Table
from opus_core.indicator_framework.image_types import GeotiffMap
from opus_core.indicator_framework.image_types import ArcGeotiffMap
from opus_core.indicator_framework.image_types import DatasetTable

#some cache_directories and run descriptions
#cache_directory = r'Y:/urbansim_cache/run_1090.2006_11_14_12_12'
#run_description = '(run 1090 - double highway capacity 11/28/2006)'
#cache_directory = r'Y:/urbansim_cache/run_1091.2006_11_14_12_12'
#run_description = '(run 1091 - baseline 11/28/2006)'
#cache_directory = r'D:\urbansim_cache\run_1454.2006_12_12_16_28'
#run_description = '(run 1454 - travel data from quick travel model)'
cache_directory = r'D:\urbansim_cache\run_1090.2006_11_14_12_12'
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
    years = [1980, 1981, 1982],
    dataset_pool_configuration = DatasetPoolConfiguration(
        package_order=['eugene','urbansim','opus_core'],
        package_order_exceptions={},
        ),       
)
single_year_requests = [
    Table(
        attribute = 'urbansim.zone.population',
        dataset_name = 'zone',
        source_data = source_data,
        ),
    Table(
        attribute = 'urbansim.zone.number_of_jobs',
        dataset_name = 'zone',
        source_data = source_data,
        ),

    Map(
        attribute = 'urbansim.zone.population',
        scale = [1, 60000],
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
        scale = [-8000, 40000],
        attribute = 'urbansim_population_change',
        source_data = source_data,
        expression = {'operation': 'change', 
                      'operands': ['urbansim.zone.population']},
        dataset_name = 'zone',
        ),
    Map(
        scale = [-2000, 40000],
        attribute = 'urbansim_employment_change',
        source_data = source_data,
        expression = {'operation': 'change', 
                      'operands': ['urbansim.zone.number_of_jobs']},
        dataset_name = 'zone',
        ),
    ]

source_data = SourceData(
    cache_directory = cache_directory,
    run_description = run_description,
    years = [1980, 1981, 1982],
    dataset_pool_configuration = DatasetPoolConfiguration(
        package_order=['eugene','urbansim','opus_core'],
        package_order_exceptions={},
        ),       
)

multi_year_requests = [
    Table(
        attribute = 'alldata.aggregate_all(urbansim.gridcell.residential_units, function=sum)',
        dataset_name = 'alldata',
        source_data = source_data,
        name = 'residential_units'
        ),
    Chart(
        attribute = 'alldata.aggregate_all(urbansim.gridcell.residential_units, function=sum)',
        dataset_name = 'alldata',
        source_data = source_data,
        name = 'residential_units'
        ),
    Table(
        attribute = 'alldata.aggregate_all(urbansim.gridcell.number_of_jobs, function=sum)',
        dataset_name = 'alldata',
        source_data = source_data,
        name =  'number_of_jobs'
        ),

    ]

if __name__ == '__main__':
    from opus_core.indicator_framework.core import IndicatorFactory

    IndicatorFactory().create_indicators(
        indicators = single_year_requests,
        display_error_box = False, 
        show_results = True)   
    IndicatorFactory().create_indicators(
        indicators = multi_year_requests,
        display_error_box = False, 
        show_results = True)   