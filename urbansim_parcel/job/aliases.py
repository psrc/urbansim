# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

aliases = [
   "zone_id = job.disaggregate(urbansim_parcel.building.zone_id)",
   "parcel_id = job.disaggregate(building.parcel_id)",
   "grid_id = job.disaggregate(urbansim_parcel.building.grid_id)",
   "is_untaken_non_home_based_job = numpy.logical_and(job.number_of_agents(person)==0, job.building_type==2)",   
   "is_untaken_home_based_job = numpy.logical_and(job.number_of_agents(person)==0, job.building_type==1)",
   "faz_id = job.disaggregate(urbansim_parcel.building.faz_id)",
   "dummy_id = urbansim_parcel.job.faz_id * 100 + job.sector_id",
   "large_area_id = job.disaggregate(parcel.large_area_id, intermediates=[building])"
           ]