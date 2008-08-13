#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

cache_directory = r'C:\opus\data\seattle_parcel\runs\run_4836.2008_01_15_16_02'
run_description = 'none'

source_data = SourceData(
    cache_directory = cache_directory,
    run_description = run_description,
    years = range(2000,2031,1),
    dataset_pool_configuration = DatasetPoolConfiguration(
        package_order=['seattle_parcel', 'psrc_parcel','urbansim_parcel', 'psrc', 'urbansim','opus_core'],
        package_order_exceptions={},
        ),       
)

#single_year_requests = [
#
#   DatasetTable(
#       source_data = source_data,
#       dataset_name = 'faz',
#       name = 'test',
#       attributes = [ 
#         'employment=faz.aggregate(urbansim_parcel.building.number_of_jobs, intermediates=[parcel, zone])',                   
#       ],
#       #exclude_condition = '==0' #exclude_condition now accepts opus expressions
#   ),
#
#    ]

multi_year_requests = [
    Table(
        attribute = 'psrc_parcel.faz_sector.total_home_based_employment',
        dataset_name = 'faz_sector',
        source_data = source_data,
        name = 'total_home_based_employment'
        ),
    Table(
        attribute = 'psrc_parcel.faz_sector.total_non_home_based_employment',
        dataset_name = 'faz_sector',
        source_data = source_data,
        name = 'total_non_home_based_employment'
        ),
    Table(
        attribute = 'psrc_parcel.faz_persons.total_number_of_households',
        dataset_name = 'faz_persons',
        source_data = source_data,
        name = 'total_number_of_households'
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