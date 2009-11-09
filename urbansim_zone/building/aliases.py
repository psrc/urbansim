# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE
aliases = [
        "number_of_households = building.number_of_agents(household)",
        "number_of_non_home_based_jobs = building.aggregate(job.home_based_status==0)",
        "number_of_home_based_jobs = building.aggregate(job.home_based_status==1)",
        "vacant_residential_units = clip_to_zero(building.residential_units - urbansim_zone.building.number_of_households)",
        "total_job_spaces = numpy.round(safe_array_divide(building.non_residential_sqft, urbansim_zone.building.building_sqft_per_job))",
        "total_non_home_based_job_spaces = numpy.round(safe_array_divide(building.non_residential_sqft, urbansim_zone.building.building_sqft_per_job))",
        "total_home_based_job_spaces = urbansim_zone.building.number_of_households",        
        "vacant_job_spaces = clip_to_zero(urbansim_zone.building.total_job_spaces - urbansim_zone.building.number_of_non_home_based_jobs)",
        "vacant_non_home_based_job_spaces = clip_to_zero(urbansim_zone.building.total_non_home_based_job_spaces - urbansim_zone.building.number_of_non_home_based_jobs)",
        "vacant_home_based_job_spaces = clip_to_zero(urbansim_zone.building.total_home_based_job_spaces - urbansim_zone.building.number_of_home_based_jobs)",
        "is_residential = building.disaggregate(building_type.is_residential)",
        "occupied_residential_spaces = urbansim_zone.building.is_residential * urbansim_zone.building.number_of_households",
        "occupied_non_residential_spaces = numpy.logical_not(urbansim_zone.building.is_residential) * urbansim_zone.building.number_of_non_home_based_jobs * urbansim_zone.building.building_sqft_per_job",
        "occupied_spaces = urbansim_zone.building.occupied_residential_spaces + urbansim_zone.building.occupied_non_residential_spaces",
        "total_spaces = urbansim_zone.building.is_residential * building.residential_units + numpy.logical_not(urbansim_zone.building.is_residential) * urbansim_zone.building.non_residential_sqft",
        "developable_residential_units_capacity = clip_to_zero(building.residential_units_capacity - building.residential_units)",
        "developable_non_residential_sqft_capacity = clip_to_zero(building.non_residential_sqft_capacity - building.non_residential_sqft)",
           ]
