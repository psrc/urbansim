# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

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
cache_directory = r'/workspace/urbansim_cache/eugene_gridcell/base_year_data/'

source_data = SourceData(
    cache_directory = cache_directory,
    run_description = run_description,
    years = [1980,],   # 2002,],#  2005, 2007, 2010, 2020, 2030],
    dataset_pool_configuration = DatasetPoolConfiguration(
        package_order=['sanfrancisco','urbansim','opus_core'],
        ),       
)
single_year_requests = [
       Map(
       source_data = source_data,
       dataset_name = 'gridcell',
       name = 'Tract Indicators',
       attribute =  'gridcell.residential_units',
       ),

       DatasetTable(
       source_data = source_data,
       dataset_name = 'gridcell',
       name = 'Tract Indicators',
       output_type='csv',
       attributes = [ 
                     'gridcell.residential_units',
       ]),

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
