# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 
                   
aliases = [
           "is_untaken=job.number_of_agents(person)==0",
           "is_untaken_home_based_job=numpy.logical_and(job.home_based_status==1, psrc_parcel.job.is_untaken)",
           "is_untaken_non_home_based_job=numpy.logical_and(job.home_based_status==0, psrc_parcel.job.is_untaken)",
           "new_zone_id = job.disaggregate(parcel.new_zone_id, intermediates=[building])",
           "city_id = job.disaggregate(parcel.city_id, intermediates=[building])"
           ]
