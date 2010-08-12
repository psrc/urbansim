# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

aliases = [
      "large_area_id = building.disaggregate(parcel.large_area_id)",
      "number_of_home_based_jobs = building.aggregate(job.home_based_status==1)",
      "number_of_non_home_based_jobs = building.aggregate(job.home_based_status==0)",
      "total_home_based_job_space = urbansim_parcel.building.total_home_based_job_space",
      "total_non_home_based_job_space = urbansim_parcel.building.total_non_home_based_job_space",
      "vacant_home_based_job_space = urbansim_parcel.building.vacant_home_based_job_space",
      "vacant_non_home_based_job_space = urbansim_parcel.building.vacant_non_home_based_job_space",
      "large_area_id = building.disaggregate(parcel.large_area_id)",
           ]