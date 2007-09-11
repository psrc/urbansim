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
from opus_core.indicator_framework.storage_location.database import Database


run_description = '(baseline 08/09/2007)'
cache_directory = r'/urbansim_cache/psrc_parcel/runs/run_3616.2007_09_10_11_34/'

source_data = SourceData(
    cache_directory = cache_directory,
    run_description = run_description,
    years = [2000,2005,2010],
    dataset_pool_configuration = DatasetPoolConfiguration(
        package_order=['psrc_parcel','urbansim_parcel','urbansim','opus_core'],
        package_order_exceptions={},
        ),       
)

indicators=[

#Chart(
    #source_data = source_data,
    #dataset_name = 'building',
    #attribute = 'alldata.aggregate_all(building.residential_units)',
    #),  

Table(
    source_data = source_data,
    dataset_name = 'zone',
    name = 'population',
    #operation = 'change',
    attribute = 'urbansim_parcel.zone.population',
),

Table(
    source_data = source_data,
    dataset_name = 'zone',
    name = 'households',
    #operation = 'change',
    attribute = 'zone.aggregate(urbansim_parcel.number_of_households)',
),

Table(
    source_data = source_data,
    dataset_name = 'zone',
    name = 'jobs',
    #operation = 'change',
    attribute = 'zone.aggregate(urbansim_parcel.number_of_jobs)',
),

Table(
    source_data = source_data,
    dataset_name = 'zone',
    name = 'residential_units',
    #operation = 'change',
    attribute = 'zone.aggregate(building.residential_units, intermediates=[parcel])',
),

Table(
    source_data = source_data,
    dataset_name = 'zone',
    name = 'nonresidential_sqft',
    #operation = 'change',
    attribute = 'zone.aggregate(building.nonresidential_sqft, intermediates=[parcel])'
),


#DatasetTable(
    ##source_data = source_data,
    #dataset_name = 'alldata',
    #name =  'number_of_jobs',
    #operation = 'change',
    #source_data = source_data,    attributes = [
        #'alldata.aggregate_all(urbansim_parcel.parcel.population)',
        ##'alldata.aggregate_all(urbansim_parcel.number_of_households)',
        ##'alldata.aggregate_all(urbansim_parcel.number_of_jobs)',
        ##'alldata.aggregate_all(building.residential_units, intermediates=[parcel])',
        ##'alldata.aggregate_all(building.nonresidential_sqft, intermediates=[parcel])'
    #],
#),
]
from opus_core.indicator_framework.core.indicator_factory import IndicatorFactory

IndicatorFactory().create_indicators(
     indicators = indicators,
     display_error_box = False, 
     show_results = True)    