# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

# The shares are computed as: 
# number of buildings of that building type / total number of buildings
# and scaled to give sum=1

sampled_shares = {
# shares computed on estimation data
# 10/18/2010
4: 0.085271,
11:0.014908,
12:0.221228,
19:0.678593,
}

observed_shares = {
# shares computed on observed data (or the baseyear)
#2000 buildings
#4: 0.080947425, #condo
#11:0.019761348, #mobile home
#12:0.230847302, #mfh
#19:0.668443925, #sfh

#2006 buildings, 10/18/2010
4: 0.095,
11:0.0187,
12:0.2392,
19:0.6470,
}

share_pattern = "%s * (urbansim.building.building_type_id == %s)"
observed_share_var = []
sampled_share_var = []
for k, v in observed_shares.iteritems():
    observed_share_var.append( share_pattern % (v, k) )
    assert k in sampled_shares
    sampled_share_var.append( share_pattern % (sampled_shares[k], k) )

observed_share_var = "observed_share=" + '+'.join(observed_share_var)
sampled_share_var = "sampled_share=" + '+'.join(sampled_share_var)
      
aliases = [
           "dummy_id=building.building_type_id * 100 + building.disaggregate(faz.large_area_id, intermediates=[zone, parcel])",
       observed_share_var,
       sampled_share_var,
       "wesml_sampling_correction_variable = safe_array_divide(psrc_parcel.building.observed_share, psrc_parcel.building.sampled_share)",
       "district_id = building.disaggregate(zone.district_id, intermediates=[parcel])",
       "city_id = building.disaggregate(parcel.city_id)",
      "new_zone_id = building.disaggregate(parcel.new_zone_id)",
      "census_block_group_id = building.disaggregate(census_block.census_block_group_id, intermediates=[parcel])",
      "census_block_id = building.disaggregate(parcel.census_block_id)",
      "tractcity_id = building.disaggregate(parcel.tractcity_id)",
      "number_of_home_based_jobs = building.aggregate(job.home_based_status==1)",
      "number_of_non_home_based_jobs = building.aggregate(job.home_based_status==0)",
      "total_home_based_job_space = urbansim_parcel.building.total_home_based_job_space",
      "total_non_home_based_job_space = psrc_parcel.building.job_capacity_computed_if_necessary",
      "vacant_home_based_job_space = clip_to_zero(psrc_parcel.building.total_home_based_job_space - psrc_parcel.building.number_of_home_based_jobs)",
      "vacant_non_home_based_job_space = clip_to_zero(psrc_parcel.building.total_non_home_based_job_space - psrc_parcel.building.number_of_non_home_based_jobs)",
      "fraction_occupied_by_non_home_based_jobs = safe_array_divide(psrc_parcel.building.number_of_non_home_based_jobs, psrc_parcel.building.total_non_home_based_job_space)",
      "has_vacancy_for_new_sector = numpy.logical_or(numpy.logical_and(psrc_parcel.building.fraction_occupied_by_non_home_based_jobs < 0.5, psrc_parcel.building.vacant_non_home_based_job_space > 20), psrc_parcel.building.number_of_non_home_based_jobs == 0)",
      "residential_land_area = building.disaggregate(safe_array_divide(psrc_parcel.parcel.total_residential_land_area_from_constraints, psrc_parcel.parcel.residential_units)) * building.residential_units"
           ]
