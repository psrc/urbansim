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

run_description = '(run 23 - baseline 02/05/2007)'
cache_directory = r'/workspace/urbansim_cache/sanfrancisco/run_23.2007_02_05_01_48'

source_data = SourceData(
    cache_directory = cache_directory,
    run_description = run_description,
    years = [2000,2001],
    dataset_pool_configuration = DatasetPoolConfiguration(
        package_order=['sanfrancisco','urbansim','opus_core'],
        package_order_exceptions={},
        ),
)

single_year_requests = [
       DatasetTable(
       source_data = source_data,
       dataset_name = 'district14',
       #name = '',
       attributes = [ 
#                                     '0_worker_households=district14.aggregate(sanfrancisco.zone.number_of_households_with_0_workers)',
#                                     '1_worker_households=district14.aggregate(sanfrancisco.zone.number_of_households_with_1_workers)',
#                                     '2_worker_households=district14.aggregate(sanfrancisco.zone.number_of_households_with_2_workers)',
#                                     '3_worker_households=district14.aggregate(sanfrancisco.zone.number_of_households_with_3_workers)',
#                                     '4_worker_households=district14.aggregate(sanfrancisco.zone.number_of_households_with_4_workers)',
#                                     '5_worker_households=district14.aggregate(sanfrancisco.zone.number_of_households_with_5_workers)',
#                                     '6_worker_households=district14.aggregate(sanfrancisco.zone.number_of_households_with_6_workers)',
#                                     '7_worker_households=district14.aggregate(sanfrancisco.zone.number_of_households_with_7_workers)',
#                                     'total_households=district14.aggregate(sanfrancisco.zone.number_of_households)',
#                                     'cie_sector_employment=district14.aggregate(sanfrancisco.zone.employment_of_sector_cie)',
#                                     'med_sector_employment=district14.aggregate(sanfrancisco.zone.employment_of_sector_med)',
#                                     'mips_sector_employment=district14.aggregate(sanfrancisco.zone.employment_of_sector_mips)',
#                                     'pdr_sector_employment=district14.aggregate(sanfrancisco.zone.employment_of_sector_pdr)',
#                                     'retail_ent_sector_employment=district14.aggregate(sanfrancisco.zone.employment_of_sector_retail_ent)',
#                                     'visitor_sector_employment=district14.aggregate(sanfrancisco.zone.employment_of_sector_visitor)',
#                                     'total_employment=district14.aggregate(sanfrancisco.zone.employment)',
       ],
       exclude_condition = '==0' 
   ),

       DatasetTable(
       source_data = source_data,
       dataset_name = 'district24',
       #name = '',
       attributes = [ 
#                                     '0_worker_households=district24.aggregate(sanfrancisco.zone.number_of_households_with_0_workers)',
#                                     '1_worker_households=district24.aggregate(sanfrancisco.zone.number_of_households_with_1_workers)',
#                                     '2_worker_households=district24.aggregate(sanfrancisco.zone.number_of_households_with_2_workers)',
#                                     '3_worker_households=district24.aggregate(sanfrancisco.zone.number_of_households_with_3_workers)',
#                                     '4_worker_households=district24.aggregate(sanfrancisco.zone.number_of_households_with_4_workers)',
#                                     '5_worker_households=district24.aggregate(sanfrancisco.zone.number_of_households_with_5_workers)',
#                                     '6_worker_households=district24.aggregate(sanfrancisco.zone.number_of_households_with_6_workers)',
#                                     '7_worker_households=district24.aggregate(sanfrancisco.zone.number_of_households_with_7_workers)',
#                                     'total_households=district24.aggregate(sanfrancisco.zone.number_of_households)',
#                                     'cie_sector_employment=district24.aggregate(sanfrancisco.zone.employment_of_sector_cie)',
#                                     'med_sector_employment=district24.aggregate(sanfrancisco.zone.employment_of_sector_med)',
#                                     'mips_sector_employment=district24.aggregate(sanfrancisco.zone.employment_of_sector_mips)',
#                                     'pdr_sector_employment=district24.aggregate(sanfrancisco.zone.employment_of_sector_pdr)',
#                                     'retail_ent_sector_employment=district24.aggregate(sanfrancisco.zone.employment_of_sector_retail_ent)',
#                                     'visitor_sector_employment=district24.aggregate(sanfrancisco.zone.employment_of_sector_visitor)',
#                                     'total_employment=district24.aggregate(sanfrancisco.zone.employment),'
       ],
       exclude_condition = '==0' 
   ),

       DatasetTable(
       source_data = source_data,
       dataset_name = 'tract2000',
       #name = '',
       attributes = [ 
                                     '0_worker_households=tract2000.aggregate(sanfrancisco.zone.number_of_households_with_0_workers)',
                                     '1_worker_households=tract2000.aggregate(sanfrancisco.zone.number_of_households_with_1_workers)',
                                     '2_worker_households=tract2000.aggregate(sanfrancisco.zone.number_of_households_with_2_workers)',
                                     '3_worker_households=tract2000.aggregate(sanfrancisco.zone.number_of_households_with_3_workers)',
                                     '4_worker_households=tract2000.aggregate(sanfrancisco.zone.number_of_households_with_4_workers)',
                                     '5_worker_households=tract2000.aggregate(sanfrancisco.zone.number_of_households_with_5_workers)',
                                     '6_worker_households=tract2000.aggregate(sanfrancisco.zone.number_of_households_with_6_workers)',
                                     '7_worker_households=tract2000.aggregate(sanfrancisco.zone.number_of_households_with_7_workers)',
                                     'total_households=tract2000.aggregate(sanfrancisco.zone.number_of_households)',
                                     'cie_sector_employment=tract2000.aggregate(sanfrancisco.zone.employment_of_sector_cie)',
                                     'med_sector_employment=tract2000.aggregate(sanfrancisco.zone.employment_of_sector_med)',
                                     'mips_sector_employment=tract2000.aggregate(sanfrancisco.zone.employment_of_sector_mips)',
                                     'pdr_sector_employment=tract2000.aggregate(sanfrancisco.zone.employment_of_sector_pdr)',
                                     'retail_ent_sector_employment=tract2000.aggregate(sanfrancisco.zone.employment_of_sector_retail_ent)',
                                     'visitor_sector_employment=tract2000.aggregate(sanfrancisco.zone.employment_of_sector_visitor)',
                                     'total_employment=tract2000.aggregate(sanfrancisco.zone.employment)',
       ],
       exclude_condition = '==0' 
   ),

]

multi_year_requests[
    Table(
        dataset_name = 'district14',
        source_data = source_data,
        attribute = 'district14.aggregate(sanfrancisco.zone.population)',
        name = 'population'
        ),
    
    Table(
        dataset_name = 'district14',
        source_data = source_data,
        attribute = 'district14.aggregate(sanfrancisco.zone.employment)',
        name = 'employment'
    ),
    
    Table(
        dataset_name = 'alldata',
        source_data = source_data,
        attribute = "alldata.aggregate_all(sanfrancisco.zone.number_of_jobs)",
        name = "total_employment"
    ),

    Table(
        dataset_name = 'alldata',
        source_data = source_data,
        attribute = 'alldata.aggregate_all(sanfrancisco.zone.population)',
        name = 'population'
    ),
]

# finally, run the requests
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
