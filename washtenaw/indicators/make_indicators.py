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

# script to produce a number of Washtenaw indicators -- 
# this illustrates using traits-based configurations programatically


from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.indicator_framework.source_data import SourceData
from opus_core.indicator_framework.image_types.matplotlib_map import Map
from opus_core.indicator_framework.image_types.matplotlib_chart import Chart
from opus_core.indicator_framework.image_types.table import Table
from opus_core.indicator_framework.image_types.geotiff_map import GeotiffMap
from opus_core.indicator_framework.image_types.arcgeotiff_map import ArcGeotiffMap
from opus_core.indicator_framework.image_types.dataset_table import DatasetTable

#cache_directory = r'C:\urbansim_cache\workshop\2006_08_28_16_58'
cache_directory = '/Users/borning/urbansim_cache/workshop/2006_08_28_16_58'
run_description = '(baseline run without travel model)'

source_data = SourceData(
    cache_directory = cache_directory,
    run_description = run_description,
    years = [2000],
    dataset_pool_configuration = DatasetPoolConfiguration(
        package_order=['washtenaw','urbansim','opus_core'],
        package_order_exceptions={},
        ),       
)

single_year_requests = [
    Map(
        source_data = source_data,
        dataset_name = 'gridcell',
        attribute = 'urbansim.gridcell.population',
        scale = [0,800])
]

source_data = SourceData(
    cache_directory = cache_directory,
    run_description = run_description,
    years = [2000],
    dataset_pool_configuration = DatasetPoolConfiguration(
        package_order=['washtenaw','urbansim','opus_core'],
        package_order_exceptions={},
        ),       
)

multi_year_requests = [
    Table(
        source_data = source_data,
        dataset_name = 'alldata',
        attribute = 'alldata.aggregate_all(urbansim.gridcell.residential_units,function=sum)',
        name = 'Residential_Units',  
    ),
    Table(
        source_data = source_data,
        dataset_name = 'alldata',
        attribute = 'alldata.aggregate_all(urbansim.gridcell.commercial_sqft,function=sum)',
        name = 'Commercial_SQFT',  
    ),        
    Table(
        source_data = source_data,
        dataset_name = 'alldata',
        attribute = 'alldata.aggregate_all(urbansim.gridcell.industrial_sqft,function=sum)',
        name = 'Industrial_SQFT',  
    ),        
    Table(
        source_data = source_data,
        dataset_name = 'alldata',
        attribute = 'alldata.aggregate_all(urbansim.gridcell.is_developed,function=sum)',
        name = 'Developed_Cells',  
    ),        
    Table(
        source_data = source_data,
        dataset_name = 'alldata',
        name = 'residential_vacancy_rate',  
        expression = {
           'operation':'divide',
           'operands':['alldata.aggregate_all(urbansim.gridcell.vacant_residential_units,function=sum)',
                       'alldata.aggregate_all(urbansim.gridcell.residential_units,function=sum)']
        }
    ),            
    Table(
        source_data = source_data,
        dataset_name = 'alldata',
        name = 'commercial_vacancy_rate',  
        expression = {
           'operation':'divide',
           'operands':['alldata.aggregate_all(urbansim.gridcell.vacant_commercial_sqft,function=sum)',
                       'alldata.aggregate_all(urbansim.gridcell.commercial_sqft,function=sum)']
        }
    ),      
    Table(
        source_data = source_data,
        dataset_name = 'alldata',
        name = 'industrial_vacancy_rate',  
        expression = {
           'operation':'divide',
           'operands':['alldata.aggregate_all(urbansim.gridcell.vacant_industrial_sqft,function=sum)',
                       'alldata.aggregate_all(urbansim.gridcell.industrial_sqft,function=sum)']
        }
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