# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 
aliases = ['is_worker = person.employment_status > 0',
           'is_worker_without_job = numpy.logical_and(urbansim_parcel.person.is_worker, person.job_id <= 0)',
           'is_worker_with_job = numpy.logical_and(urbansim_parcel.person.is_worker, person.job_id > 0)',
           'is_non_home_based_worker = numpy.logical_and(urbansim_parcel.person.is_worker,  (person.work_at_home!=1))',
           'is_non_home_based_worker_with_job = numpy.logical_and(urbansim_parcel.person.is_non_home_based_worker, person.job_id > 0)',
           'is_non_home_based_worker_without_job = numpy.logical_and(urbansim_parcel.person.is_non_home_based_worker, person.job_id <= 0)',
           'zone_id=person.disaggregate(urbansim_parcel.household.zone_id)',
           'workplace_zone_id=person.disaggregate(urbansim_parcel.job.zone_id)',
           'building_id = person.disaggregate(household.building_id)',
           'is_placed_non_home_based_worker_with_job = numpy.logical_and(urbansim_parcel.person.is_non_home_based_worker_with_job, urbansim_parcel.person.building_id > 0)',
           'parcel_id = person.disaggregate(urbansim_parcel.household.parcel_id)'
           ]