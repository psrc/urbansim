# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

# The shares are computed as: 
# number of buildings of that building type / total number of buildings
# and scaled to give sum=1

sampled_shares = {
# shares computed on estimation data
#4: 0.007159353,
#11: 0.02517321,
#12: 0.037413395, 
#19: 0.930254042,

#psrc_2005_parcel_baseyear_change_20080408.households_for_estimation
4: 0.059584914,
11:0.014728855,
12:0.131667039,
19:0.794019192,

#psrc_activity2006_ver2.households_for_estimation 080415
#4: 0.060772314,
#11:0.014138003,
#12:0.130196243,
#19:0.794893437,
}

observed_shares = {
# shares computed on observed data (or the baseyear)
#2000 buildings
4: 0.080947425, #condo
11:0.019761348, #mobile home
12:0.230847302, #mfh
19:0.668443925, #sfh

#2005 buildings
#4: 0.095030049,
#11:0.018702192,
#12:0.239230620,
#19:0.647037140,
}




      
observed_share_var = "observed_building_type_share = %s * (urbansim.building.building_type_id == %s)" % (observed_shares[observed_shares.keys()[0]],
                                                                                                     observed_shares.keys()[0])
sampled_share_var = "sampled_building_type_share = %s * (urbansim.building.building_type_id == %s)" % (sampled_shares[sampled_shares.keys()[0]],
                                                                                                     sampled_shares.keys()[0])
for bt in observed_shares.keys()[1:len(observed_shares.keys())]:
    observed_share_var = observed_share_var + " + %s * (urbansim.building.building_type_id == %s)" % (observed_shares[bt], bt)
    sampled_share_var = sampled_share_var + " + %s * (urbansim.building.building_type_id == %s)" % (sampled_shares[bt], bt)
                   
aliases = [
           "dummy_id=building.building_type_id * 100 + building.disaggregate(faz.large_area_id, intermediates=[zone, parcel])",
       observed_share_var,
       sampled_share_var,
       "wesml_sampling_correction_variable = safe_array_divide(psrc_parcel.building.observed_building_type_share, psrc_parcel.building.sampled_building_type_share)",
       "district_id = building.disaggregate(zone.district_id, intermediates=[parcel])",
       "city_id = building.disaggregate(parcel.city_id)",
      "number_of_home_based_jobs = building.aggregate(job.home_based_status==1)",
      "number_of_non_home_based_jobs = building.aggregate(job.home_based_status==0)",
      "total_home_based_job_space = urbansim_parcel.building.total_home_based_job_space",
      "total_non_home_based_job_space = psrc_parcel.building.job_capacity_computed_if_necessary",
      "vacant_home_based_job_space = clip_to_zero(psrc_parcel.building.total_home_based_job_space - psrc_parcel.building.number_of_home_based_jobs)",
      "vacant_non_home_based_job_space = clip_to_zero(psrc_parcel.building.total_non_home_based_job_space - psrc_parcel.building.number_of_non_home_based_jobs)",
           ]
