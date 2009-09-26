# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE
aliases = [
        "number_of_households = building.number_of_agents(household)",
        "number_of_non_home_based_jobs = building.aggregate(job.home_based_status==0)",
        "vacant_residential_units = clip_to_zero(building.residential_units - urbansim_zone.building.number_of_households)",
        "total_job_spaces = building.non_residential_sqft / urbansim_zone.building.building_sqft_per_job",
        "vacant_job_spaces = clip_to_zero(urbansim_zone.building.total_job_spaces - urbansim_zone.building.number_of_non_home_based_jobs)",
        
           ]
