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
from opus_core.indicator_framework.source_data import SourceData
from opus_core.indicator_framework.image_types.matplotlib_map import Map
from opus_core.indicator_framework.image_types.matplotlib_chart import Chart
from opus_core.indicator_framework.image_types.table import Table
from opus_core.indicator_framework.image_types.geotiff_map import GeotiffMap
from opus_core.indicator_framework.image_types.arcgeotiff_map import ArcGeotiffMap
from opus_core.indicator_framework.image_types.dataset_table import DatasetTable
from opus_core.indicator_framework.image_types.matplotlib_lorenz_curve import LorenzCurve

#some cache_directories and run descriptions
#cache_directory = r'Y:/urbansim_cache/run_1090.2006_11_14_12_12'
#run_description = '(run 1090 - double highway capacity 11/28/2006)'
#cache_directory = r'Y:/urbansim_cache/run_1091.2006_11_14_12_12'
#run_description = '(run 1091 - baseline 11/28/2006)'
#cache_directory = r'D:\urbansim_cache\run_1454.2006_12_12_16_28'
#run_description = '(run 1454 - travel data from quick travel model)'
cache_directory = r'H:\urbansim_cache\2007_04_12_21_23'
run_description = '(run 2600 - tutorial run)'
#cache_directory = r'Y:\urbansim_cache\run_1431.2006_12_08_09_45'
#run_description = '(run 1431 - baseyear travel data from travel model run)'
#cache_directory = r'D:\urbansim_cache\run_1154.2006_11_17_20_06'
#run_description = '(run 1154 - no ugb + double highway capacity 11/28/2006)'
#cache_directory = r'D:\urbansim_cache\run_1155.2006_11_17_20_07'
#run_description = '(run 1155 - no ugb 11/28/2006)'

source_data = SourceData(
    cache_directory = cache_directory,
    run_description = run_description,
    years = [1980],
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
    LorenzCurve(attribute = 'urbansim.household.income',
                source_data = source_data,
                dataset_name = 'household'
        )
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
    ]

if __name__ == '__main__':
    from opus_core.indicator_framework.indicator_factory import IndicatorFactory

    IndicatorFactory().create_indicators(
        indicators = single_year_requests,
        display_error_box = False, 
        show_results = True)   
    IndicatorFactory().create_indicators(
        indicators = multi_year_requests,
        display_error_box = False, 
        show_results = True)   
