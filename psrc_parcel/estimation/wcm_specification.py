# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

all_variables = [
#    "hh_income = person.disaggregate(household.income)",
#    "hh_size = person.disaggregate(household.persons)",
#    "person.age",
#    "person.work_at_home",
#    "person.edu",         
    "hh_income_x_job_is_in_employment_sector_group_fires = person.disaggregate(household.income) * urbansim.job.is_in_employment_sector_group_fires",    
    "psrc_parcel.person_x_job.income_and_am_total_transit_time_walk_from_home_to_work",

    "edu_x_job_is_in_employment_sector_group_basic = person.edu * urbansim.job.is_in_employment_sector_group_basic",    
    "edu_x_job_is_in_employment_sector_group_retail = person.edu * urbansim.job.is_in_employment_sector_group_retail",    
    "edu_x_job_is_in_employment_sector_group_services = person.edu * urbansim.job.is_in_employment_sector_group_services",    
    "edu_x_job_is_in_employment_sector_group_manu = person.edu * urbansim.job.is_in_employment_sector_group_manu",    
    "edu_x_job_is_in_employment_sector_group_wtcu = person.edu * urbansim.job.is_in_employment_sector_group_wtcu",    
    "edu_x_job_is_in_employment_sector_group_fires = person.edu * urbansim.job.is_in_employment_sector_group_fires",    
    "edu_x_job_is_in_employment_sector_group_gov = person.edu * urbansim.job.is_in_employment_sector_group_gov",    
    "edu_x_job_is_in_employment_sector_group_edu = person.edu * urbansim.job.is_in_employment_sector_group_edu",    

#    "travel_time_from_home_to_work_driving = psrc_parcel.person_x_job.travel_time_hbw_am_drive_alone_from_home_to_work",
#    "travel_time_from_home_to_work_transit = psrc_parcel.person_x_job.am_total_transit_time_walk_from_home_to_work",
    
#    "psrc_parcel.person_x_job.home_area_type_is_same_as_workplace_area_type",
#    "psrc_parcel.person_x_job.home_area_type_1_workplace_area_type_1",
#    "psrc_parcel.person_x_job.home_area_type_1_workplace_area_type_2",
#    "psrc_parcel.person_x_job.home_area_type_1_workplace_area_type_3",
#    "psrc_parcel.person_x_job.home_area_type_1_workplace_area_type_4",
#    "psrc_parcel.person_x_job.home_area_type_2_workplace_area_type_1",
#    "psrc_parcel.person_x_job.home_area_type_2_workplace_area_type_2",
#    "psrc_parcel.person_x_job.home_area_type_2_workplace_area_type_3",
#    "psrc_parcel.person_x_job.home_area_type_2_workplace_area_type_4",
#    "psrc_parcel.person_x_job.home_area_type_3_workplace_area_type_1",
#    "psrc_parcel.person_x_job.home_area_type_3_workplace_area_type_2",
#    "psrc_parcel.person_x_job.home_area_type_3_workplace_area_type_3",
#    "psrc_parcel.person_x_job.home_area_type_3_workplace_area_type_4",
#    "psrc_parcel.person_x_job.home_area_type_4_workplace_area_type_1",
#    "psrc_parcel.person_x_job.home_area_type_4_workplace_area_type_2",
#    "psrc_parcel.person_x_job.home_area_type_4_workplace_area_type_3",
#    "psrc_parcel.person_x_job.home_area_type_4_workplace_area_type_4",

    "lnempden = ln( (job.disaggregate(urbansim_parcel.zone.number_of_jobs_per_acre, intermediates=[parcel, building])).astype(float32) )",

    ]

specification = {}

specification = {
    "_definition_": all_variables,                               
    -2:
        [

#"psrc_parcel.person_x_job.travel_time_hbw_am_drive_alone_from_home_to_work",
"psrc_parcel.person_x_job.logsum_hbw_am_from_home_to_work",
#         "psrc_parcel.person_x_job.am_total_transit_time_walk_from_home_to_work",
         #'lnempden',

#"euclidean_distance_in_miles = psrc_parcel.person_x_job.euclidean_distance_from_home_to_work/1609.3",
"psrc_parcel.person_x_job.network_distance_from_home_to_work",
#"psrc_parcel.person_x_job.travel_cost_from_home_to_work",

"psrc_parcel.person_x_job.home_district_is_same_as_workplace_district",

"home_dist_19_workplace_dist_19=(person.disaggregate(zone.district_id)==19) * (job.disaggregate(zone.district_id)==19)",
#"home_19_workplace_ne_19=(person.disaggregate(zone.district_id)==19) * (job.disaggregate(zone.district_id)!=19)",

# "psrc_parcel.person_x_job.home_area_type_is_same_as_workplace_area_type",
          ## area_types: 1-metropolitan cities; 2-core & larger suburban cities; 
          ##             3-smaller suburban and unincorporated UGA
          ##             4-rural areas 
        #"psrc_parcel.person_x_job.home_area_type_1_workplace_area_type_1",
        "psrc_parcel.person_x_job.home_area_type_1_workplace_area_type_2",
        #+!"psrc_parcel.person_x_job.home_area_type_1_workplace_area_type_3",
        #+!"psrc_parcel.person_x_job.home_area_type_1_workplace_area_type_4",

        #"psrc_parcel.person_x_job.home_area_type_2_workplace_area_type_1",
        #"psrc_parcel.person_x_job.home_area_type_2_workplace_area_type_2",
        #"psrc_parcel.person_x_job.home_area_type_2_workplace_area_type_3",
        #"psrc_parcel.person_x_job.home_area_type_2_workplace_area_type_4", 

        #"psrc_parcel.person_x_job.home_area_type_3_workplace_area_type_1",
        #"psrc_parcel.person_x_job.home_area_type_3_workplace_area_type_2",
        #"psrc_parcel.person_x_job.home_area_type_3_workplace_area_type_3",
        #"psrc_parcel.person_x_job.home_area_type_3_workplace_area_type_4",

        #"psrc_parcel.person_x_job.home_area_type_4_workplace_area_type_1",
        "psrc_parcel.person_x_job.home_area_type_4_workplace_area_type_2",
        #"psrc_parcel.person_x_job.home_area_type_4_workplace_area_type_3",
        #"psrc_parcel.person_x_job.home_area_type_4_workplace_area_type_4",

"edu_x_job_is_in_employment_sector_group_basic",    
"edu_x_job_is_in_employment_sector_group_retail",    
#"edu_x_job_is_in_employment_sector_group_manu",    
    #"edu_x_job_is_in_employment_sector_group_wtcu",    
"edu_x_job_is_in_employment_sector_group_fires",    
    #"edu_x_job_is_in_employment_sector_group_gov",    
"edu_x_job_is_in_employment_sector_group_edu",    

   #'hh_income_x_job_is_in_employment_sector_group_fires',
    ],                             
}
