# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2012 ETH Zurich
# See project SustainCity

aliases = [        
           'is_untaken_non_home_based_job = numpy.logical_and(job.number_of_agents(person)==0)' #variation of urbansim_parcel

   #copy of urbansim_parcel       
  # "zone_id = job.disaggregate(urbansim_parcel.building.zone_id)",
  # "parcel_id = job.disaggregate(building.parcel_id)",
  # "grid_id = job.disaggregate(urbansim_parcel.building.grid_id)",
  # "is_untaken_non_home_based_job = numpy.logical_and(job.number_of_agents(person)==0, job.building_type==2)",   
  # "is_untaken_home_based_job = numpy.logical_and(job.number_of_agents(person)==0, job.building_type==1)",
  # "faz_id = job.disaggregate(urbansim_parcel.building.faz_id)",
  # "dummy_id = urbansim_parcel.job.faz_id * 100 + job.sector_id",
  # "large_area_id = job.disaggregate(parcel.large_area_id, intermediates=[building])",
  # "is_home_based = job.home_based_status==1",
  # "is_non_home_based = numpy.logical_not(urbansim_parcel.job.is_home_based)"
  # "building_type = job.disaggregate(building.building_type_id)"
   ]