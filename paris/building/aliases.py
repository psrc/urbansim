# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE
aliases = [
        "dept_id = building.dept",
        "zgp_id = building.disaggregate(zone.zgp_id)",
        "vacant_non_home_based_job_spaces = clip_to_zero(urbansim_zone.building.total_non_home_based_job_spaces - paris.building.number_of_non_home_based_jobs)",
        "number_of_non_home_based_jobs = building.aggregate((establishment.employment)*(establishment.disappeared==0))",
        "occupied_residential_spaces = urbansim_zone.building.is_residential * urbansim_zone.building.number_of_households",
        "occupied_non_residential_spaces = numpy.logical_not(urbansim_zone.building.is_residential) * paris.building.number_of_non_home_based_jobs * urbansim_zone.building.building_sqft_per_job",
        "occupied_spaces = paris.building.occupied_residential_spaces + paris.building.occupied_non_residential_spaces",
        "vacant_res_units = ((building.residential_units - building.number_of_agents(household))>0)*(building.residential_units - building.number_of_agents(household)) +  ((building.residential_units - building.number_of_agents(household))<1)"
           ]
