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
    dataset_name = 'large_area',
    name = 'population',
    #operation = 'change',
    attribute = 'large_area.aggregate(urbansim_parcel.zone.population, intermediates=[faz])',
),

Table(
    source_data = source_data,
    dataset_name = 'large_area',
    name = 'households',
    #operation = 'change',
    attribute = 'large_area.aggregate(urbansim_parcel.zone.number_of_households, intermediates=[faz])',
),

Table(
    source_data = source_data,
    dataset_name = 'large_area',
    name = 'jobs',
    #operation = 'change',
    attribute = 'large_area.aggregate(urbansim_parcel.zone.number_of_jobs, intermediates=[faz])',
),


Table(
    source_data = source_data,
    dataset_name = 'large_area',
    name = 'residential_units',
    #operation = 'change',
    attribute = 'large_area.aggregate(building.residential_units, intermediates=[parcel,zone,faz])',
),

Table(
    source_data = source_data,
    dataset_name = 'large_area',
    name = 'nonresidential_sqft',
    #operation = 'change',
    attribute = 'large_area.aggregate(building.non_residential_sqft, intermediates=[parcel,zone,faz])'
),

#  Table(
#      source_data = source_data,
#      dataset_name = 'zone',
#      name = 'population',
#      #operation = 'change',
#      attribute = 'urbansim_parcel.zone.population',
#  ),

#  Table(
#      source_data = source_data,
#      dataset_name = 'zone',
#      name = 'households',
#      #operation = 'change',
#      attribute = 'zone.aggregate(urbansim_parcel.number_of_households)',
#  ),

#  Table(
#      source_data = source_data,
#      dataset_name = 'zone',
#      name = 'jobs',
#      #operation = 'change',
#      attribute = 'zone.aggregate(urbansim_parcel.number_of_jobs)',
#  ),

#  Table(
#      source_data = source_data,
#      dataset_name = 'zone',
#      name = 'residential_units',
#      #operation = 'change',
#      attribute = 'zone.aggregate(building.residential_units, intermediates=[parcel])',
#  ),

#  Table(
#      source_data = source_data,
#      dataset_name = 'zone',
#      name = 'nonresidential_sqft',
#      #operation = 'change',
#      attribute = 'zone.aggregate(building.nonresidential_sqft, intermediates=[parcel])'
#  ),

# Table(
#     source_data = source_data,
#     dataset_name = 'zone',
#     name = 'residential_units',
#     #operation = 'change',
#     attribute = 'zone.aggregate(building.residential_units, intermediates=[parcel])',
# ),

# Table(
#     source_data = source_data,
#     dataset_name = 'zone',
#     name = 'nonresidential_sqft',
#     #operation = 'change',
#     attribute = 'zone.aggregate(building.nonresidential_sqft, intermediates=[parcel])'
# ),


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

# DatasetTable(
#     source_data = source_data,
#     dataset_name = 'development_project_proposal',
#     name = 'sfr_proposal_cons',
#     attributes = [
# #       'development_project_proposal.proposal_id',
#        'development_project_proposal.parcel_id',
#        'development_project_proposal.template_id',
#        'fit_contraint = (urbansim_parcel.development_project_proposal.is_allowed_by_constraint).astype(int32)',
#        'fit_size = (urbansim_parcel.development_project_proposal.is_size_fit).astype(int32)',
#        'urbansim_parcel.development_project_proposal.units_proposed',
#        'urbansim_parcel.development_project_proposal.land_area_taken',
#        'parcel_sqft=development_project_proposal.disaggregate(parcel.parcel_sqft)',
#        'template_sqft_min=development_project_proposal.disaggregate(development_template.land_sqft_min)',
#        'template_sqft_max=development_project_proposal.disaggregate(development_template.land_sqft_max)',
#        'template_far=development_project_proposal.disaggregate(urbansim_parcel.development_template.far)',
#        'min_far=development_project_proposal.disaggregate(urbansim_parcel.parcel.min_far_capacity_for_generic_land_use_type_1)',
#        'max_far=development_project_proposal.disaggregate(urbansim_parcel.parcel.max_far_capacity_for_generic_land_use_type_1)',
#        'template_units_per_acre=development_project_proposal.disaggregate(urbansim_parcel.development_template.units_per_acre)',
#        'min_units_per_acre=development_project_proposal.disaggregate(urbansim_parcel.parcel.min_units_per_acre_capacity_for_generic_land_use_type_1)',
#        'max_units_per_acre=development_project_proposal.disaggregate(urbansim_parcel.parcel.max_units_per_acre_capacity_for_generic_land_use_type_1)',
#     ],
#     #exclude_condition = {'building_type_id':'!=19'}
# ),

]
from opus_core.indicator_framework.core.indicator_factory import IndicatorFactory

IndicatorFactory().create_indicators(
     indicators = indicators,
     display_error_box = False, 
     show_results = True)    
