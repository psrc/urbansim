# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.indicator_framework.core.source_data import SourceData

#from opus_core.indicator_framework.image_types.matplotlib_map import Map
#from opus_core.indicator_framework.image_types.matplotlib_chart import Chart
from opus_core.indicator_framework.image_types.table import Table
from opus_core.indicator_framework.image_types.geotiff_map import GeotiffMap
from opus_core.indicator_framework.image_types.dataset_table import DatasetTable
#from opus_core.indicator_framework.image_types.matplotlib_lorenzcurve import LorenzCurve
from opus_core.indicator_framework.core.indicator_factory import IndicatorFactory
import os, sys

""" 
This script generates residential_units_capacity and non_residential_sqft_capacity 
from urbansim_parcel data for use with development project location choice model in urbansim_zone
"""
cache_directory = 'X:\\psrc_parcel\\base_year_data\\'
output_type = 'tab'
storage_location = os.path.join(cache_directory, 'indicators')
year = 2000

run_description = 'Create residential_units and non_residential_sqft capacity for development project location choice model in urbansim_zone'

source_data = SourceData(
    cache_directory = cache_directory,
    run_description = run_description,
    years = [int(year)],
    dataset_pool_configuration = DatasetPoolConfiguration(
        package_order=['psrc_parcel','urbansim_parcel','psrc', 'urbansim','opus_core'],
        ),       
)

attrs_by_glu = []  
# this loop create indicators for each generic_land_type from 1 to 8
for glu_id in range(1, 9):
    attrs_by_glu += [

        ## existing units/sqft
        "existing_units_glu%s = zone.aggregate(parcel.aggregate(building.residential_units) * (parcel.disaggregate(land_use_type.generic_land_use_type_id)==%s) )" % (glu_id, glu_id),
        "existing_sqft_glu%s = zone.aggregate(parcel.aggregate(building.non_residential_sqft) * (parcel.disaggregate(land_use_type.generic_land_use_type_id)==%s) ) " % (glu_id, glu_id),
        
        ## existing units/job spaces excluding redevelopable parcels
        "unredev_existing_units_glu%s = zone.aggregate(parcel.aggregate(building.residential_units) * numpy.logical_not(psrc_parcel.parcel.is_redevelopable) * (parcel.disaggregate(land_use_type.generic_land_use_type_id)==%s) )" % (glu_id, glu_id),
        "unredev_existing_sqft_glu%s = zone.aggregate(parcel.aggregate(building.non_residential_sqft) * numpy.logical_not(psrc_parcel.parcel.is_redevelopable) * (parcel.disaggregate(land_use_type.generic_land_use_type_id)==%s) )" % (glu_id, glu_id),
        
        ## units and sqft on redevelopable parcels
        "redev_units_glu%s=zone.aggregate(urbansim_parcel.parcel.max_units_per_acre_capacity_for_generic_land_use_type_%s * ( parcel.parcel_sqft / 43560.0 ) * (psrc_parcel.parcel.is_redevelopable).astype(int32) )" % (glu_id, glu_id),
        "redev_sqft_glu%s=zone.aggregate(urbansim_parcel.parcel.max_far_capacity_for_generic_land_use_type_%s * parcel.parcel_sqft * (psrc_parcel.parcel.is_redevelopable).astype(int32) ) " % (glu_id, glu_id),

        ## units and sqft on vacant/agriculture parcels
        "va_units_glu%s = zone.aggregate( urbansim_parcel.parcel.max_units_per_acre_capacity_for_generic_land_use_type_%s * ( parcel.parcel_sqft / 43560.0 ) * numpy.logical_or( parcel.disaggregate(land_use_type.land_use_name)=='vacant',  parcel.disaggregate(land_use_type.land_use_name)=='agriculture') )" % (glu_id, glu_id), 
        "va_sqft_glu%s = zone.aggregate( urbansim_parcel.parcel.max_far_capacity_for_generic_land_use_type_%s * parcel.parcel_sqft * numpy.logical_or( parcel.disaggregate(land_use_type.land_use_name)=='vacant',  parcel.disaggregate(land_use_type.land_use_name)=='agriculture') ) " % (glu_id, glu_id),        
    ]

indicators=[
   DatasetTable(
       attributes = attrs_by_glu,
       dataset_name = 'zone',
       source_data = source_data,
       name = 'development_capacity',
       output_type = output_type,
       storage_location = storage_location
       ),
]

IndicatorFactory().create_indicators(
     indicators = indicators,
     display_error_box = False, 
     show_results = False)    
