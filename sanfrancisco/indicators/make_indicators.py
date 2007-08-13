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


run_description = '(baseline 06/28/2007)'
cache_directory = r'/urbansim_cache/sanfrancisco/07_06_28_17_18_21/'

source_data = SourceData(
    cache_directory = cache_directory,
    run_description = run_description,
    years = [2001],
    dataset_pool_configuration = DatasetPoolConfiguration(
        package_order=['sanfrancisco','urbansim','opus_core'],
        package_order_exceptions={},
        ),       
)
single_year_requests = [

       DatasetTable(
       source_data = source_data,
       dataset_name = 'tract2000',
       name = 'Tract Indicators',
       output_type='csv',
       attributes = [ 
                     'households_with_0_workers=tract2000.aggregate(sanfrancisco.building.number_of_households_with_0_workers, intermediates=[parcel])',
                     'households_with_1_worker =tract2000.aggregate(sanfrancisco.building.number_of_households_with_1_workers, intermediates=[parcel])',
                     'households_with_2_workers=tract2000.aggregate(sanfrancisco.building.number_of_households_with_2_workers, intermediates=[parcel])',
                     'households_with_3_workers=tract2000.aggregate(sanfrancisco.building.number_of_households_with_3_workers, intermediates=[parcel])',
                     'households_with_4_workers=tract2000.aggregate(sanfrancisco.building.number_of_households_with_4_workers, intermediates=[parcel])',
                     'households_with_5_workers=tract2000.aggregate(sanfrancisco.building.number_of_households_with_5_workers, intermediates=[parcel])',
                     'households_with_6_workers=tract2000.aggregate(sanfrancisco.building.number_of_households_with_6_workers, intermediates=[parcel])',
                     'households_with_7_workers=tract2000.aggregate(sanfrancisco.building.number_of_households_with_7_workers, intermediates=[parcel])',
                     'total_households=tract2000.aggregate(sanfrancisco.building.number_of_households, intermediates=[parcel])',
                     'total_population=tract2000.aggregate(sanfrancisco.building.population, intermediates=[parcel])',                                     
                     'sector_1_employment=tract2000.aggregate(sanfrancisco.building.employment_of_sector_1, intermediates=[parcel])',
                     'sector_2_employment=tract2000.aggregate(sanfrancisco.building.employment_of_sector_2, intermediates=[parcel])',
                     'sector_3_employment=tract2000.aggregate(sanfrancisco.building.employment_of_sector_3, intermediates=[parcel])',
                     'sector_4_employment=tract2000.aggregate(sanfrancisco.building.employment_of_sector_4, intermediates=[parcel])',
                     'sector_5_employment=tract2000.aggregate(sanfrancisco.building.employment_of_sector_5, intermediates=[parcel])',
                     'sector_6_employment=tract2000.aggregate(sanfrancisco.building.employment_of_sector_6, intermediates=[parcel])',
                     'total_employment=tract2000.aggregate(sanfrancisco.building.employment, intermediates=[parcel])',
       ],
       exclude_condition = '==0' 
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
       exclude_condition = '==0' 
),

    ]

source_data = SourceData(
    cache_directory = cache_directory,
    run_description = run_description,
    years = [2001,2002,2003,2004,2005],
    dataset_pool_configuration = DatasetPoolConfiguration(
        package_order=['sanfrancisco','urbansim','opus_core'],
        package_order_exceptions={},
        ),       
)

multi_year_requests = [
    #Chart(
        #attribute = 'sanfrancisco.district14.aggregate(building.residential_units,intermediates=[parcel])',
        #dataset_name = 'district14',
        #source_data = source_data,
        #),
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