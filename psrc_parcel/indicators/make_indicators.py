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

from opus_core.indicator_framework.image_types import Map, Chart, GeotiffMap, ArcGeotiffMap, LorenzCurve
from opus_core.indicator_framework.image_types import Table, DatasetTable

run_description = '(baseline 08/09/2007)'
cache_directory = r'/urbansim_cache/psrc_parcel/run_3375.2007_08_09_10_40/'

source_data = SourceData(
    cache_directory = cache_directory,
    run_description = run_description,
    years = [2001,2005],
    dataset_pool_configuration = DatasetPoolConfiguration(
        package_order=['psrc_parcel','urbansim_parcel','urbansim','opus_core'],
        package_order_exceptions={},
        ),       
)

indicators=[
DatasetTable(
    source_data = source_data,
    dataset_name = 'zone',
    name = 'pop_and_emp_sqft',
    attributes = [ 
      'urbansim_parcel.zone.population',
      'urbansim_parcel.zone.number_of_jobs',                     
    ],
    exclude_condition = '==0' 
),
]
from opus_core.indicator_framework.core import IndicatorFactory

IndicatorFactory().create_indicators(
     indicators = indicators,
     display_error_box = False, 
     show_results = True)    