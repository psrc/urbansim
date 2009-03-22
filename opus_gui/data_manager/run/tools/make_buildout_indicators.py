# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
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


def opusRun(progressCB,logCB,params):

    params_dict = {}
    for key, val in params.iteritems():
        params_dict[str(key)] = str(val)

    cache_directory = params_dict['cache_directory']
    output_type = params_dict['output_type']
    storage_location = params_dict['storage_location']
    year = params_dict['year']
    
    if output_type == '':
        output_type = 'tab'

    """ Prerequisite:
    1. run buildingout_query.sql to create building_sqft_per_job_by_zone_generic_land_use_type_id table, or similar table for other geography 
    2. cache the table to the cache that needs to create buildout indicators for
    3. get/create building_sqft_per_job_by_zone_generic_land_use_type_id_dataset.py (in urbansim_parcel/datasets)
    4. active/planned/proposed projects are cached in development_project_proposals and development_project_proposal_components
    5. add is_redevelopable attribute to parcel
    """
    
    run_description = 'Create indicators for buildout analysis'
    
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
    for glu_id in range(3, 9):
        attrs_by_glu += [
            ## existing
            "existing_job_spaces_glu%s = zone.aggregate(parcel.aggregate(building.non_residential_sqft)) / zone.disaggregate(building_sqft_per_job_by_zone_generic_land_use_type_id.building_sqft_per_job_glu%s)" % (glu_id, glu_id),
            
            ## existing units/job spaces excluding redevelopable parcels
            "existing_job_spaces_unredev_glu%s=zone.aggregate(parcel.aggregate(building.non_residential_sqft) * numpy.logical_not(urbansim_parcel.parcel.is_redevelopable).astype(int32) ) / zone.disaggregate(building_sqft_per_job_by_zone_generic_land_use_type_id.building_sqft_per_job_glu%s)" % (glu_id, glu_id),
            
            ## redevelopment
            "redev_buildout_units_glu%s=zone.aggregate(urbansim_parcel.parcel.max_units_per_acre_capacity_for_generic_land_use_type_%s * parcel.parcel_sqft * (urbansim_parcel.parcel.is_redevelopable).astype(int32) )" % (glu_id, glu_id),
            "redev_buildout_job_spaces_glu%s=zone.aggregate(urbansim_parcel.parcel.max_far_capacity_for_generic_land_use_type_%s * parcel.parcel_sqft * (urbansim_parcel.parcel.is_redevelopable).astype(int32) ) / zone.disaggregate(building_sqft_per_job_by_zone_generic_land_use_type_id.building_sqft_per_job_glu%s)" % (glu_id, glu_id, glu_id),
    
            ## active(status_id==1)/planned(status_id==3)/proposed(status_id==2)
            "proposed_job_spaces_glu%s = zone.aggregate(development_project_proposal.aggregate(urbansim_parcel.development_project_proposal_component.units_proposed * (numpy.logical_not(urbansim_parcel.development_project_proposal_component.is_residential)).astype(int32)) * (urbansim_parcel.development_project_proposal.status_id==2).astype(int32), intermediates=[parcel] ) / zone.disaggregate(building_sqft_per_job_by_zone_generic_land_use_type_id.building_sqft_per_job_glu%s)" % (glu_id, glu_id), 
    
            ## vacant/agriculture buildout
            "va_buildout_glu%s = zone.aggregate( urbansim_parcel.parcel.max_units_per_acre_capacity_for_generic_land_use_type_%s * ( parcel.parcel_sqft / 43560.0 ) * ( parcel.number_of_agents(development_project_proposal) == 0) * numpy.logical_or( parcel.disaggregate(land_use_type.land_use_name)=='vacant',  parcel.disaggregate(land_use_type.land_use_name)=='agriculture') )" % (glu_id, glu_id), 
            "va_buildout_job_spaces_glu%s = zone.aggregate( urbansim_parcel.parcel.max_far_capacity_for_generic_land_use_type_%s * parcel.parcel_sqft * ( parcel.number_of_agents(development_project_proposal) == 0) * numpy.logical_or( parcel.disaggregate(land_use_type.land_use_name)=='vacant',  parcel.disaggregate(land_use_type.land_use_name)=='agriculture') )  / zone.disaggregate(building_sqft_per_job_by_zone_generic_land_use_type_id.building_sqft_per_job_glu%s)" % (glu_id, glu_id, glu_id),        
        ]

    for glu_id in range(1, 3):
        attrs_by_glu += [
            ## existing
            "existing_job_spaces_glu%s = zone.aggregate(parcel.aggregate(building.non_residential_sqft)) / zone.disaggregate(building_sqft_per_job_by_zone_generic_land_use_type_id.building_sqft_per_job_glu%s)" % (glu_id, glu_id),
            
            ## existing units/job spaces excluding redevelopable parcels
            "existing_job_spaces_unredev_glu%s=zone.aggregate(parcel.aggregate(building.non_residential_sqft) * numpy.logical_not(urbansim_parcel.parcel.is_redevelopable).astype(int32) ) / zone.disaggregate(building_sqft_per_job_by_zone_generic_land_use_type_id.building_sqft_per_job_glu%s)" % (glu_id, glu_id),
            
            ## redevelopment
            "redev_buildout_units_glu%s=zone.aggregate(urbansim_parcel.parcel.max_units_per_acre_capacity_for_generic_land_use_type_%s * parcel.parcel_sqft * (urbansim_parcel.parcel.is_redevelopable).astype(int32) )" % (glu_id, glu_id),
#            "redev_buildout_job_spaces_glu%s=zone.aggregate(urbansim_parcel.parcel.max_far_capacity_for_generic_land_use_type_%s * parcel.parcel_sqft * (urbansim_parcel.parcel.is_redevelopable).astype(int32) ) / zone.disaggregate(building_sqft_per_job_by_zone_generic_land_use_type_id.building_sqft_per_job_glu%s)" % (glu_id, glu_id, glu_id),
    
            ## active(status_id==1)/planned(status_id==3)/proposed(status_id==2)
            "proposed_job_spaces_glu%s = zone.aggregate(development_project_proposal.aggregate(urbansim_parcel.development_project_proposal_component.units_proposed * (numpy.logical_not(urbansim_parcel.development_project_proposal_component.is_residential)).astype(int32)) * (urbansim_parcel.development_project_proposal.status_id==2).astype(int32), intermediates=[parcel] ) / zone.disaggregate(building_sqft_per_job_by_zone_generic_land_use_type_id.building_sqft_per_job_glu%s)" % (glu_id, glu_id), 
    
            ## vacant/agriculture buildout
            "va_buildout_glu%s = zone.aggregate( urbansim_parcel.parcel.max_units_per_acre_capacity_for_generic_land_use_type_%s * ( parcel.parcel_sqft / 43560.0 ) * ( parcel.number_of_agents(development_project_proposal) == 0) * numpy.logical_or( parcel.disaggregate(land_use_type.land_use_name)=='vacant',  parcel.disaggregate(land_use_type.land_use_name)=='agriculture') )" % (glu_id, glu_id), 
#            "va_buildout_job_spaces_glu%s = zone.aggregate( urbansim_parcel.parcel.max_far_capacity_for_generic_land_use_type_%s * parcel.parcel_sqft * ( parcel.number_of_agents(development_project_proposal) == 0) * numpy.logical_or( parcel.disaggregate(land_use_type.land_use_name)=='vacant',  parcel.disaggregate(land_use_type.land_use_name)=='agriculture') )  / zone.disaggregate(building_sqft_per_job_by_zone_generic_land_use_type_id.building_sqft_per_job_glu%s)" % (glu_id, glu_id, glu_id),        
        ]
    
    
    
    indicators=[
       DatasetTable(
           attributes = [
               ### indicators don't need to iterate by generic_land_use_type
               ## existing
               "existing_units = zone.aggregate(urbansim_parcel.parcel.residential_units)",
               #"existing_job_spaces_glu1 = zone.aggregate(parcel.aggregate(building.non_residential_sqft)) / zone.disaggregate(building_sqft_per_job_by_zone_generic_land_use_type_id.building_sqft_per_job_glu1)",
    
               ## existing units/job spaces excluding redevelopable parcels
               "existing_units_unredev=zone.aggregate(urbansim_parcel.parcel.residential_units * numpy.logical_not(urbansim_parcel.parcel.is_redevelopable).astype(int32) )",
               #"existing_job_spaces_unredev_glu1=zone.aggregate(parcel.aggregate(building.non_residential_sqft) * numpy.logical_not(urbansim_parcel.parcel.is_redevelopable).astype(int32) ) / zone.disaggregate(building_sqft_per_job_by_zone_generic_land_use_type_id.building_sqft_per_job_glu1)",
    
               ## redevelopment
               #"redev_buildout_units_glu1=zone.aggregate(urbansim_parcel.parcel.max_units_per_acre_capacity_for_generic_land_use_type_1 * parcel.parcel_sqft * (urbansim_parcel.parcel.is_redevelopable).astype(int32) )",
               #"redev_buildout_job_spaces_glu1=zone.aggregate(urbansim_parcel.parcel.max_far_capacity_for_generic_land_use_type_1 * parcel.parcel_sqft * (urbansim_parcel.parcel.is_redevelopable).astype(int32) ) / zone.disaggregate(building_sqft_per_job_by_zone_generic_land_use_type_id.building_sqft_per_job_glu1)",
    
               ## active(status_id==1)/planned(status_id==3)/proposed(status_id==2)
               "proposed_units = zone.aggregate(development_project_proposal.aggregate(urbansim_parcel.development_project_proposal_component.units_proposed * (urbansim_parcel.development_project_proposal_component.is_residential).astype(int32)) * (urbansim_parcel.development_project_proposal.status_id==2).astype(int32), intermediates=[parcel] )",
               #"proposed_job_spaces_glu1 = zone.aggregate(development_project_proposal.aggregate(urbansim_parcel.development_project_proposal_component.units_proposed * (numpy.logical_not(urbansim_parcel.development_project_proposal_component.is_residential)).astype(int32)) * (urbansim_parcel.development_project_proposal.status_id==2).astype(int32), intermediates=[parcel] ) / zone.disaggregate(building_sqft_per_job_by_zone_generic_land_use_type_id.building_sqft_per_job_glu1)",
    
               ## vacant/agriculture buildout
               #"va_buildout_glu1 = zone.aggregate( urbansim_parcel.parcel.max_units_per_acre_capacity_for_generic_land_use_type_1 * parcel.parcel_sqft * ( parcel.number_of_agents(development_project_proposal) == 0) * numpy.logical_or( parcel.disaggregate(land_use_type.land_use_name)=='vacant',  parcel.disaggregate(land_use_type.land_use_name)=='agriculture') )", 
               #"va_buildout_job_spaces_glu1 = zone.aggregate( urbansim_parcel.parcel.max_far_capacity_for_generic_land_use_type_1 * parcel.parcel_sqft * ( parcel.number_of_agents(development_project_proposal) == 0) * numpy.logical_or( parcel.disaggregate(land_use_type.land_use_name)=='vacant',  parcel.disaggregate(land_use_type.land_use_name)=='agriculture') )  / zone.disaggregate(building_sqft_per_job_by_zone_generic_land_use_type_id.building_sqft_per_job_glu1)",        
               ] + attrs_by_glu,
           dataset_name = 'zone',
           source_data = source_data,
           name = 'zone_buildout',
           output_type = output_type,
           storage_location = storage_location
           ),
    ]
    
    IndicatorFactory().create_indicators(
         indicators = indicators,
         display_error_box = False, 
         show_results = False)    
