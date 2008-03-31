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
from opus_core.indicator_framework.core.source_data import SourceData

from opus_core.indicator_framework.image_types.matplotlib_map import Map
from opus_core.indicator_framework.image_types.matplotlib_chart import Chart
from opus_core.indicator_framework.image_types.table import Table
from opus_core.indicator_framework.image_types.geotiff_map import GeotiffMap
from opus_core.indicator_framework.image_types.dataset_table import DatasetTable
from opus_core.indicator_framework.image_types.matplotlib_lorenzcurve import LorenzCurve
from opus_core.database_management.database_configuration import DatabaseConfiguration


#some cache_directories and run descriptions
#cache_directory = r'Y:/urbansim_cache/run_1090.2006_11_14_12_12'
#run_description = '(run 1090 - double highway capacity 11/28/2006)'
#cache_directory = r'Y:/urbansim_cache/run_1091.2006_11_14_12_12'
#run_description = '(run 1091 - baseline 11/28/2006)'
#cache_directory = r'D:\urbansim_cache\run_1454.2006_12_12_16_28'
#run_description = '(run 1454 - travel data from quick travel model)'
#cache_directory = r'D:\urbansim_cache\run_1090.2006_11_14_12_12'
cache_directory = r'C:\opus\opus_data\seattle_parcel\run_4836.2008_01_15_16_02'
run_description = 'none'
#cache_directory = r'Y:\urbansim_cache\run_1431.2006_12_08_09_45'
#run_description = '(run 1431 - baseyear travel data from travel model run)'
#cache_directory = r'D:\urbansim_cache\run_1154.2006_11_17_20_06'
#run_description = '(run 1154 - no ugb + double highway capacity 11/28/2006)'
#cache_directory = r'D:\urbansim_cache\run_1155.2006_11_17_20_07'
#run_description = '(run 1155 - no ugb 11/28/2006)'

source_data = SourceData(
    cache_directory = cache_directory,
    run_description = run_description,
    years = [2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030],
    dataset_pool_configuration = DatasetPoolConfiguration(
        package_order=['seattle_parcel', 'psrc_parcel','urbansim_parcel', 'psrc', 'urbansim','opus_core'],
        package_order_exceptions={},
        ),       
)
#single_year_requests = [
#
#   DatasetTable(
#       years = [2000-2005],
#       source_data = source_data,
#       dataset_name = 'faz',
#       name = 'test',
#       attributes = [ 
#         'employment=faz.aggregate(urbansim_parcel.building.number_of_jobs, intermediates=[parcel, zone])',
#         #'employment=large_area.aggregate(urbansim_parcel.building.number_of_jobs, intermediates=[parcel, zone, faz])'                     
#       ],
#       #exclude_condition = '==0' #exclude_condition now accepts opus expressions
#   ),
#
#    ]

multi_year_requests = [
    Table(
        attribute = 'employment=faz.aggregate(urbansim_parcel.building.number_of_jobs, intermediates=[parcel, zone])',
        dataset_name = 'faz',
        source_data = source_data,
        name = 'test'
        ),
    ]

if __name__ == '__main__':
    from opus_core.indicator_framework.core.indicator_factory import IndicatorFactory

#    IndicatorFactory().create_indicators(
#        indicators = single_year_requests,
#        display_error_box = False, 
#        show_results = True)   
    IndicatorFactory().create_indicators(
        indicators = multi_year_requests,
        display_error_box = False, 
        show_results = True)   