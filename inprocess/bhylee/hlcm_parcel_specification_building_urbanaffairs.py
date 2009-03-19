# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

specification = {}

specification = {
        0:   #submodel_id
            [

            "is_condo_residential = building.disaggregate(building_type.building_type_name)=='condo_residential'",
            "is_multi_family_residential = building.disaggregate(building_type.building_type_name)=='multi_family_residential'",
            #"is_single_family_residential = building.disaggregate(building_type.building_type_name)=='single_family_residential'",
            "is_pre_1940 = building.year_built < 1940",
            "ln_avg_bedrooms_per_unit = ln(building.number_of_bedrooms/building.residential_units)",
            "ln_avg_building_sf_per_unit = ln(building.building_sqft/building.residential_units)",
            #"ln_building_sf_per_bedroom = ln(building.building_sqft/building.number_of_bedrooms)",
            "ln_avg_value_per_unit = ln(building.total_value/building.residential_units)",
            #"ln_parcel_sf = ln(building.disaggregate(parcel.parcel_sqft))",
            "ln_parcel_sf_per_unit = ln(building.disaggregate(parcel.parcel_sqft)/building.residential_units)",
            "ln_residential_units = ln(building.residential_units)",
            
            #"ln_emp_15min_hbw_drive_alone = building.disaggregate(psrc.zone.ln_employment_within_15_minutes_travel_time_hbw_am_drive_alone)",
            #"ln_emp_30min_hbw_drive_alone = building.disaggregate(psrc.zone.ln_employment_within_30_minutes_travel_time_hbw_am_drive_alone)",
            #"ln_emp_30min_hbw_transit_walk = building.disaggregate(psrc.zone.ln_employment_within_30_minutes_travel_time_hbw_am_transit_walk)",
            "ln_emp_45min_hbw_transit_walk = building.disaggregate(psrc.zone.ln_employment_within_45_minutes_travel_time_hbw_am_transit_walk)",
            #"gen_cost_wt_access_to_emp_hbw_drive_alone = building.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone)",
            #"gen_cost_wt_access_to_emp_hbw_transit_walk = building.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk)",
            #"trip_wt_avg_time_hbw_drive_alone = building.disaggregate(psrc.zone.trip_weighted_average_time_hbw_from_home_am_drive_alone)",
            "ln_trip_wt_avg_time_hbw_drive_alone = ln(building.disaggregate(psrc.zone.trip_weighted_average_time_hbw_from_home_am_drive_alone))",
            #"trip_wt_avg_time_hbw_transit_walk = building.disaggregate(psrc.zone.trip_weighted_average_time_hbw_from_home_am_transit_walk)",
            "ln_trip_wt_avg_time_hbw_transit_walk = ln(building.disaggregate(psrc.zone.trip_weighted_average_time_hbw_from_home_am_transit_walk))",
            "ln_number_of_jobs_within_walking_distance = ln(building.disaggregate(psrc.parcel.number_of_jobs_within_walking_distance))",
            #"ln_number_of_commercial_jobs_within_walking_distance = ln(building.disaggregate(psrc.parcel.number_of_commercial_jobs_within_walking_distance))",
            "ln_residential_units_within_walking_distance = ln(building.disaggregate(psrc.parcel.residential_units_within_walking_distance))",


            #"cars_x_is_condo_residential = household.cars * urbansim.building.is_condo_residential",
            #"cars_x_is_multi_family_residential = household.cars * urbansim.building.is_multi_family_residential",
            ##"cars_x_is_single_family_residential = household.cars * urbansim.building.is_single_family_residential",
            #"cars_x_ln_avg_building_sf_per_unit = household.cars * ln(building.building_sqft/building.residential_units)",
            #"cars_x_ln_avg_value_per_unit = household.cars * ln(building.total_value/building.residential_units)",
            ##"cars_x_ln_parcel_sf = household.cars * ln(urbansim.building.parcel_sqft)",
            #"cars_x_ln_parcel_sf_per_unit = household.cars * ln(urbansim.building.parcel_sqft_per_unit)",
            #"cars_x_ln_residential_units = household.cars * ln(building.residential_units)",

            #"children_x_is_condo_residential = household.children * urbansim.building.is_condo_residential",
            #"children_x_is_multi_family_residential = household.children * urbansim.building.is_multi_family_residential",
            ##"children_x_is_single_family_residential = household.children * urbansim.building.is_single_family_residential",
            #"children_x_ln_avg_building_sf_per_unit = household.children * ln(building.building_sqft/building.residential_units)",
            #"children_x_ln_avg_value_per_unit = household.children * ln(building.total_value/building.residential_units)",
            ##"children_x_ln_parcel_sf = household.children * ln(urbansim.building.parcel_sqft)",
            ##"children_x_ln_parcel_sf_per_unit = household.children * ln(urbansim.building.parcel_sqft_per_unit)",
            #"children_x_ln_residential_units = household.children * ln(building.residential_units)",

            "income_x_is_condo_residential = household.income * urbansim.building.is_condo_residential",
            "income_x_is_multi_family_residential = household.income * urbansim.building.is_multi_family_residential",
            #"income_x_is_single_family_residential = household.income * urbansim.building.is_single_family_residential",
            #"income_x_is_pre_1940 = household.income * (building.year_built < 1940)",
            "income_x_ln_avg_bedrooms_per_unit = household.income * ln(building.number_of_bedrooms/building.residential_units)",
            #"income_x_ln_avg_building_sf_per_unit = household.income * ln(building.building_sqft/building.residential_units)",
            #"income_x_ln_building_sf_per_bedroom = household.income * ln(building.building_sqft/building.number_of_bedrooms)",
            "income_x_ln_avg_value_per_unit = household.income * ln(building.total_value/building.residential_units)",
            #"income_inv_x_ln_avg_value_per_unit = 1/household.income * ln(building.total_value/building.residential_units)",
            #"income_x_ln_parcel_sf = household.income * ln(urbansim.building.parcel_sqft)",
            #"income_x_ln_parcel_sf_per_unit = household.income * ln(urbansim.building.parcel_sqft_per_unit)",
            #"income_x_ln_residential_units = household.income * ln(building.residential_units)",
            #"income_x_ln_emp_30min_hbw_drive_alone = household.income * urbansim.building.ln_employment_within_30_minutes_travel_time_hbw_am_drive_alone",            
            #"income_x_ln_emp_30min_hbw_transit_walk = household.income * urbansim.building.ln_employment_within_30_minutes_travel_time_hbw_am_transit_walk",
            #"income_x_ln_emp_45min_hbw_transit_walk = household.income * urbansim.building.ln_employment_within_45_minutes_travel_time_hbw_am_transit_walk",
            #"income_inv_x_ln_emp_45min_hbw_transit_walk = 1/household.income * urbansim.building.ln_employment_within_45_minutes_travel_time_hbw_am_transit_walk",            
            #"income_x_ln_number_of_jobs_within_walking_distance = household.income * ln(urbansim.building.number_of_jobs_within_walking_distance)",
            "income_inv_x_ln_number_of_jobs_within_walking_distance = 1/household.income * urbansim.building.number_of_jobs_within_walking_distance",            
            
            "persons_x_is_condo_residential = household.persons * urbansim.building.is_condo_residential",
            "persons_x_is_multi_family_residential = household.persons * urbansim.building.is_multi_family_residential",
            #"persons_x_is_single_family_residential = household.persons * urbansim.building.is_single_family_residential",            
            #"persons_x_ln_avg_bedrooms_per_unit = household.persons * ln(building.number_of_bedrooms/building.residential_units)",
            "persons_x_ln_avg_building_sf_per_unit = household.persons * ln(building.building_sqft/building.residential_units)",
            #"persons_x_ln_avg_value_per_unit = household.persons * ln(building.total_value/building.residential_units)",
            #"persons_x_ln_parcel_sf = household.persons * ln(urbansim.building.parcel_sqft)",
            #"persons_x_ln_parcel_sf_per_unit = household.persons * ln(urbansim.building.parcel_sqft_per_unit)",
            #"persons_x_ln_residential_units = household.persons * ln(building.residential_units)",

            #"workers_x_is_condo_residential = household.workers * urbansim.building.is_condo_residential",
            #"workers_x_is_multi_family_residential = household.workers * urbansim.building.is_multi_family_residential",
            ##"workers_x_is_single_family_residential = household.workers * urbansim.building.is_single_family_residential",            
            #"workers_x_ln_avg_building_sf_per_unit = household.workers * ln(building.building_sqft/building.residential_units)",
            #"workers_x_ln_avg_value_per_unit = household.workers * ln(building.total_value/building.residential_units)",
            ##"workers_x_ln_parcel_sf = household.workers * ln(urbansim.building.parcel_sqft)",
            #"workers_x_ln_parcel_sf_per_unit = household.workers * ln(urbansim.building.parcel_sqft_per_unit)",
            #"workers_x_ln_residential_units = household.workers * ln(building.residential_units)",
            #"workers_x_ln_emp_30min_hbw_drive_alone = household.workers * urbansim.building.ln_employment_within_30_minutes_travel_time_hbw_am_drive_alone",
            #"workers_x_ln_emp_30min_hbw_transit_walk = household.workers * urbansim.building.ln_employment_within_30_minutes_travel_time_hbw_am_transit_walk",
            #"workers_x_ln_number_of_jobs_within_walking_distance = household.workers * ln(urbansim.building.number_of_jobs_within_walking_distance)",
            #"workers_x_generalized_cost_weighted_access_to_employment_hbw_am_drive_alone = household.workers * ln(urbansim.building.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone)",
            #"workers_x_generalized_cost_weighted_access_to_employment_hbw_am_transit_walk = household.workers * ln(urbansim.building.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk)",


#variables below need to be revised and tested

            #"income_and_ln_housing_value=household.income * ln(parcel.aggregate(building.total_value))",
            #"psrc.household_x_parcel.income_and_ln_lot_sf",
            #"income_and_ln_residential_units=household.income * ln(parcel.aggregate(building.residential_units))",
            #"psrc.household_x_parcel.income_and_year_built",

            #"psrc.parcel.population_density_in_gridcell",
            #"psrc.parcel.ln_retail_sector_employment_within_walking_distance",
            #"urbansim.household_x_gridcell.income_and_year_built",
            
            #"parcel:ln_employment_within_15_minutes_travel_time_hbw_am_transit_walk = disaggregate(psrc.zone.ln_employment_within_15_minutes_travel_time_hbw_am_transit_walk)",
            #"parcel:ln_employment_within_30_minutes_travel_time_hbw_am_drive_alone = disaggregate(psrc.zone.ln_employment_within_30_minutes_travel_time_hbw_am_drive_alone)",
            #"parcel:ln_employment_within_30_minutes_travel_time_hbw_am_transit_walk = disaggregate(psrc.zone.ln_employment_within_30_minutes_travel_time_hbw_am_transit_walk)",
            #"psrc.parcel.average_household_size_within_walking_distance", #SIG
            #"psrc.parcel.housing_density_within_walking_distance", #SIG
            #"psrc.parcel.ln_retail_sector_employment_within_walking_distance", #SIG
            #"psrc.parcel.ln_service_sector_employment_within_walking_distance", #SIG
            #"psrc.parcel.ln_total_employment_within_walking_distance", #SIG
            #"psrc.parcel.number_of_commercial_jobs_within_walking_distance",
            #"psrc.parcel.number_of_industrial_jobs_within_walking_distance",
            #"psrc.parcel.number_of_high_income_households_within_walking_distance", #SIG
            #"psrc.parcel.number_of_low_income_households_within_walking_distance", #SIG
            #"psrc.parcel.number_of_mid_income_households_within_walking_distance", #SIG
            #"psrc.parcel.number_of_minority_households_within_walking_distance", #SIG
            #"psrc.parcel.number_of_not_minority_households_within_walking_distance", #SIG
            #"psrc.parcel.percent_commercial_within_walking_distance",
            #"psrc.parcel.percent_industrial_within_walking_distance",
            #"psrc.parcel.percent_mixed_use_within_walking_distance", #SIG
            #"psrc.parcel.percent_open_space_within_walking_distance",
            #"psrc.parcel.percent_residential_within_walking_distance",
            #"psrc.parcel.percent_high_income_households_within_walking_distance", #SIG
            #"psrc.parcel.percent_low_income_households_within_walking_distance", #SIG
            #"psrc.parcel.percent_mid_income_households_within_walking_distance", #SIG
            #"psrc.parcel.percent_minority_households_within_walking_distance", #SIG
            #"psrc.parcel.percent_not_minority_households_within_walking_distance", #SIG
                
            #"psrc.household_x_parcel.gridcell_housing_density_within_walking_distance_multiply_psrc_household_number_of_persons",
            #"psrc.household_x_parcel.gridcell_housing_density_within_walking_distance_multiply_urbansim_household_is_low_income",
            #"psrc.household_x_parcel.gridcell_housing_density_within_walking_distance_multiply_urbansim_household_is_minority",
            #"psrc.household_x_parcel.gridcell_housing_density_within_walking_distance_multiply_urbansim_household_is_young",
            #"psrc.household_x_parcel.gridcell_average_household_size_within_walking_distance_multiply_psrc_household_number_of_persons",
            #"psrc.household_x_parcel.gridcell_percent_mixed_use_within_walking_distance_multiply_urbansim_household_is_minority",
            #"psrc.household_x_parcel.gridcell_percent_residential_within_walking_distance_multiply_urbansim_household_is_high_income",
            #"psrc.household_x_parcel.gridcell_percent_open_space_within_walking_distance_multiply_urbansim_household_is_high_income",
            #"psrc.household_x_parcel.gridcell_percent_commercial_within_walking_distance_multiply_urbansim_household_is_high_income",
            #"psrc.household_x_parcel.gridcell_percent_industrial_within_walking_distance_multiply_urbansim_household_is_high_income",
            #"psrc.household_x_parcel.gridcell_ln_retail_sector_employment_within_walking_distance_multiply_urbansim_household_has_less_cars_than_workers",
            #"psrc.household_x_parcel.gridcell_ln_service_sector_employment_within_walking_distance_multiply_urbansim_household_has_less_cars_than_workers",
            #"psrc.household_x_parcel.gridcell_ln_total_employment_within_walking_distance_multiply_urbansim_household_has_less_cars_than_workers",
            #"psrc.household_x_parcel.gridcell_percent_high_income_households_within_walking_distance_multiply_urbansim_household_is_high_income",
            #"psrc.household_x_parcel.gridcell_percent_low_income_households_within_walking_distance_multiply_urbansim_household_is_low_income",
            #"psrc.household_x_parcel.gridcell_percent_low_income_households_within_walking_distance_multiply_urbansim_household_is_high_income",
            #"psrc.household_x_parcel.gridcell_percent_minority_households_within_walking_distance_multiply_urbansim_household_is_minority",
            #"psrc.household_x_parcel.gridcell_percent_not_minority_households_within_walking_distance_multiply_urbansim_household_is_not_minority",
            
            #"parcel:trip_weighted_average_time_hbw_from_home_am_drive_alone = disaggregate(psrc.zone.trip_weighted_average_time_hbw_from_home_am_drive_alone)",
            #"parcel:trip_weighted_average_time_hbw_from_home_am_transit_walk = disaggregate(psrc.zone.trip_weighted_average_time_hbw_from_home_am_transit_walk)",
            #"parcel:generalized_cost_weighted_access_to_employment_hbw_am_drive_alone = disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone)",
            #"psrc.parcel.travel_time_hbw_am_drive_alone_to_cbd",

            #"psrc.household_x_parcel.worker1_travel_time_hbw_am_drive_alone_from_home_to_work",
            #"psrc.household_x_parcel.worker1_am_total_transit_time_walk_from_home_to_work",
            #"psrc.household_x_parcel.worker2_travel_time_hbw_am_drive_alone_from_home_to_work",
            #"psrc.household_x_parcel.worker2_am_total_transit_time_walk_from_home_to_work",
                
            #"psrc.household_x_parcel.worker1_travel_time_hbw_am_drive_alone_from_home_to_work_if_worker_does_not_use_transit",
            #"psrc.household_x_parcel.worker1_am_total_transit_time_walk_from_home_to_work_if_worker_uses_transit",
            #"psrc.household_x_parcel.worker2_travel_time_hbw_am_drive_alone_from_home_to_work_if_worker_does_not_use_transit",
            #"psrc.household_x_parcel.worker2_am_total_transit_time_walk_from_home_to_work_if_worker_uses_transit",

            #"psrc.household_x_parcel.worker1_am_total_transit_time_walk_from_home_to_work_if_household_has_less_cars_than_nonhome_based_workers",
            #"psrc.household_x_parcel.worker2_am_total_transit_time_walk_from_home_to_work_if_household_has_less_cars_than_nonhome_based_workers",

            #"transit_accessibility.household_x_parcel.worker1_travel_time_hbw_transit_from_work_to_home",
            #"transit_accessibility.household_x_parcel.worker2_travel_time_hbw_transit_from_work_to_home",
            #"transit_accessibility.household_x_parcel.worker1_travel_time_hbw_transit_from_work_to_home_if_worker_uses_transit",
            #"transit_accessibility.household_x_parcel.worker2_travel_time_hbw_transit_from_work_to_home_if_worker_uses_transit",
            ],
"""            
        1:   #submodel_id
            [
            "ln_built_sf_unit = ln(psrc.parcel.built_sf_unit)",
            "ln_housing_value = ln(psrc.parcel.housing_value)",
            "ln_lot_sf_unit = ln(psrc.parcel.lot_sf_unit)",
            #"ln_number_of_jobs_within_walking_distance = ln(psrc.parcel.number_of_jobs_within_walking_distance)",
            #"ln_residential_units_within_walking_distance = ln(psrc.parcel.residential_units_within_walking_distance)",
            "ln_residential_units = ln(parcel.residential_units)",
            #"ln_year_built = ln(parcel.year_built)",
            #"square_year_built = parcel.year_built**2",
            
            "psrc.household_x_parcel.income_and_ln_built_sf",
            "psrc.household_x_parcel.income_and_ln_housing_value",
            #"psrc.household_x_parcel.income_and_ln_lot_sf",
            "psrc.household_x_parcel.income_and_ln_residential_units",
            #"psrc.household_x_parcel.income_and_year_built",
            #"psrc.parcel.is_pre_1940",
            #"psrc.parcel.population_density_in_gridcell",
            #"psrc.parcel.ln_retail_sector_employment_within_walking_distance",
            #"urbansim.household_x_gridcell.income_and_year_built",
            
            "parcel:ln_employment_within_15_minutes_travel_time_hbw_am_drive_alone = disaggregate(psrc.zone.ln_employment_within_15_minutes_travel_time_hbw_am_drive_alone)",
            #"parcel:ln_employment_within_15_minutes_travel_time_hbw_am_transit_walk = disaggregate(psrc.zone.ln_employment_within_15_minutes_travel_time_hbw_am_transit_walk)",
            #"parcel:ln_employment_within_30_minutes_travel_time_hbw_am_drive_alone = disaggregate(psrc.zone.ln_employment_within_30_minutes_travel_time_hbw_am_drive_alone)",
            #"parcel:ln_employment_within_30_minutes_travel_time_hbw_am_transit_walk = disaggregate(psrc.zone.ln_employment_within_30_minutes_travel_time_hbw_am_transit_walk)",
            #"psrc.parcel.average_household_size_within_walking_distance", #SIG
            #"psrc.parcel.housing_density_within_walking_distance", #SIG
            #"psrc.parcel.ln_retail_sector_employment_within_walking_distance", #SIG
            #"psrc.parcel.ln_service_sector_employment_within_walking_distance", #SIG
            #"psrc.parcel.ln_total_employment_within_walking_distance", #SIG
            #"psrc.parcel.number_of_commercial_jobs_within_walking_distance",
            #"psrc.parcel.number_of_industrial_jobs_within_walking_distance",
            #"psrc.parcel.number_of_high_income_households_within_walking_distance", #SIG
            #"psrc.parcel.number_of_low_income_households_within_walking_distance", #SIG
            #"psrc.parcel.number_of_mid_income_households_within_walking_distance", #SIG
            #"psrc.parcel.number_of_minority_households_within_walking_distance", #SIG
            #"psrc.parcel.number_of_not_minority_households_within_walking_distance", #SIG
            #"psrc.parcel.percent_commercial_within_walking_distance",
            #"psrc.parcel.percent_industrial_within_walking_distance",
            #"psrc.parcel.percent_mixed_use_within_walking_distance", #SIG
            #"psrc.parcel.percent_open_space_within_walking_distance",
            #"psrc.parcel.percent_residential_within_walking_distance",
            #"psrc.parcel.percent_high_income_households_within_walking_distance", #SIG
            #"psrc.parcel.percent_low_income_households_within_walking_distance", #SIG
            #"psrc.parcel.percent_mid_income_households_within_walking_distance", #SIG
            #"psrc.parcel.percent_minority_households_within_walking_distance", #SIG
            #"psrc.parcel.percent_not_minority_households_within_walking_distance", #SIG
                
            #"psrc.household_x_parcel.gridcell_housing_density_within_walking_distance_multiply_psrc_household_number_of_persons",
            #"psrc.household_x_parcel.gridcell_housing_density_within_walking_distance_multiply_urbansim_household_is_low_income",
            #"psrc.household_x_parcel.gridcell_housing_density_within_walking_distance_multiply_urbansim_household_is_minority",
            #"psrc.household_x_parcel.gridcell_housing_density_within_walking_distance_multiply_urbansim_household_is_young",
            #"psrc.household_x_parcel.gridcell_average_household_size_within_walking_distance_multiply_psrc_household_number_of_persons",
            #"psrc.household_x_parcel.gridcell_percent_mixed_use_within_walking_distance_multiply_urbansim_household_is_minority",
            #"psrc.household_x_parcel.gridcell_percent_residential_within_walking_distance_multiply_urbansim_household_is_high_income",
            #"psrc.household_x_parcel.gridcell_percent_open_space_within_walking_distance_multiply_urbansim_household_is_high_income",
            #"psrc.household_x_parcel.gridcell_percent_commercial_within_walking_distance_multiply_urbansim_household_is_high_income",
            #"psrc.household_x_parcel.gridcell_percent_industrial_within_walking_distance_multiply_urbansim_household_is_high_income",
            #"psrc.household_x_parcel.gridcell_ln_retail_sector_employment_within_walking_distance_multiply_urbansim_household_has_less_cars_than_workers",
            #"psrc.household_x_parcel.gridcell_ln_service_sector_employment_within_walking_distance_multiply_urbansim_household_has_less_cars_than_workers",
            #"psrc.household_x_parcel.gridcell_ln_total_employment_within_walking_distance_multiply_urbansim_household_has_less_cars_than_workers",
            #"psrc.household_x_parcel.gridcell_percent_high_income_households_within_walking_distance_multiply_urbansim_household_is_high_income",
            #"psrc.household_x_parcel.gridcell_percent_low_income_households_within_walking_distance_multiply_urbansim_household_is_low_income",
            #"psrc.household_x_parcel.gridcell_percent_low_income_households_within_walking_distance_multiply_urbansim_household_is_high_income",
            #"psrc.household_x_parcel.gridcell_percent_minority_households_within_walking_distance_multiply_urbansim_household_is_minority",
            #"psrc.household_x_parcel.gridcell_percent_not_minority_households_within_walking_distance_multiply_urbansim_household_is_not_minority",
            
            #"parcel:trip_weighted_average_time_hbw_from_home_am_drive_alone = disaggregate(psrc.zone.trip_weighted_average_time_hbw_from_home_am_drive_alone)",
            #"parcel:trip_weighted_average_time_hbw_from_home_am_transit_walk = disaggregate(psrc.zone.trip_weighted_average_time_hbw_from_home_am_transit_walk)",
            #"parcel:generalized_cost_weighted_access_to_employment_hbw_am_drive_alone = disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone)",
            #"psrc.parcel.travel_time_hbw_am_drive_alone_to_cbd",

            #"psrc.household_x_parcel.worker1_travel_time_hbw_am_drive_alone_from_home_to_work",
            #"psrc.household_x_parcel.worker1_am_total_transit_time_walk_from_home_to_work",
            #"psrc.household_x_parcel.worker2_travel_time_hbw_am_drive_alone_from_home_to_work",
            #"psrc.household_x_parcel.worker2_am_total_transit_time_walk_from_home_to_work",
                
            #"psrc.household_x_parcel.worker1_travel_time_hbw_am_drive_alone_from_home_to_work_if_worker_does_not_use_transit",
            #"psrc.household_x_parcel.worker1_am_total_transit_time_walk_from_home_to_work_if_worker_uses_transit",
            #"psrc.household_x_parcel.worker2_travel_time_hbw_am_drive_alone_from_home_to_work_if_worker_does_not_use_transit",
            #"psrc.household_x_parcel.worker2_am_total_transit_time_walk_from_home_to_work_if_worker_uses_transit",

            #"psrc.household_x_parcel.worker1_am_total_transit_time_walk_from_home_to_work_if_household_has_less_cars_than_nonhome_based_workers",
            #"psrc.household_x_parcel.worker2_am_total_transit_time_walk_from_home_to_work_if_household_has_less_cars_than_nonhome_based_workers",

            #"transit_accessibility.household_x_parcel.worker1_travel_time_hbw_transit_from_work_to_home",
            #"transit_accessibility.household_x_parcel.worker2_travel_time_hbw_transit_from_work_to_home",
            #"transit_accessibility.household_x_parcel.worker1_travel_time_hbw_transit_from_work_to_home_if_worker_uses_transit",
            #"transit_accessibility.household_x_parcel.worker2_travel_time_hbw_transit_from_work_to_home_if_worker_uses_transit",
            ],
        2:   #submodel_id
            [
            "ln_built_sf_unit = ln(psrc.parcel.built_sf_unit)",
            "ln_housing_value = ln(psrc.parcel.housing_value)",
            "ln_lot_sf_unit = ln(psrc.parcel.lot_sf_unit)",
            #"ln_number_of_jobs_within_walking_distance = ln(psrc.parcel.number_of_jobs_within_walking_distance)",
            #"ln_residential_units_within_walking_distance = ln(psrc.parcel.residential_units_within_walking_distance)",
            "ln_residential_units = ln(parcel.residential_units)",
            #"ln_year_built = ln(parcel.year_built)",
            #"square_year_built = parcel.year_built**2",
            
            "psrc.household_x_parcel.income_and_ln_built_sf",
            "psrc.household_x_parcel.income_and_ln_housing_value",
            #"psrc.household_x_parcel.income_and_ln_lot_sf",
            "psrc.household_x_parcel.income_and_ln_residential_units",
            #"psrc.household_x_parcel.income_and_year_built",
            #"psrc.parcel.is_pre_1940",
            #"psrc.parcel.population_density_in_gridcell",
            #"psrc.parcel.ln_retail_sector_employment_within_walking_distance",
            #"urbansim.household_x_gridcell.income_and_year_built",
            
            "parcel:ln_employment_within_15_minutes_travel_time_hbw_am_drive_alone = disaggregate(psrc.zone.ln_employment_within_15_minutes_travel_time_hbw_am_drive_alone)",
            #"parcel:ln_employment_within_15_minutes_travel_time_hbw_am_transit_walk = disaggregate(psrc.zone.ln_employment_within_15_minutes_travel_time_hbw_am_transit_walk)",
            #"parcel:ln_employment_within_30_minutes_travel_time_hbw_am_drive_alone = disaggregate(psrc.zone.ln_employment_within_30_minutes_travel_time_hbw_am_drive_alone)",
            #"parcel:ln_employment_within_30_minutes_travel_time_hbw_am_transit_walk = disaggregate(psrc.zone.ln_employment_within_30_minutes_travel_time_hbw_am_transit_walk)",
            #"psrc.parcel.average_household_size_within_walking_distance", #SIG
            #"psrc.parcel.housing_density_within_walking_distance", #SIG
            #"psrc.parcel.ln_retail_sector_employment_within_walking_distance", #SIG
            #"psrc.parcel.ln_service_sector_employment_within_walking_distance", #SIG
            #"psrc.parcel.ln_total_employment_within_walking_distance", #SIG
            #"psrc.parcel.number_of_commercial_jobs_within_walking_distance",
            #"psrc.parcel.number_of_industrial_jobs_within_walking_distance",
            #"psrc.parcel.number_of_high_income_households_within_walking_distance", #SIG
            #"psrc.parcel.number_of_low_income_households_within_walking_distance", #SIG
            #"psrc.parcel.number_of_mid_income_households_within_walking_distance", #SIG
            #"psrc.parcel.number_of_minority_households_within_walking_distance", #SIG
            #"psrc.parcel.number_of_not_minority_households_within_walking_distance", #SIG
            #"psrc.parcel.percent_commercial_within_walking_distance",
            #"psrc.parcel.percent_industrial_within_walking_distance",
            #"psrc.parcel.percent_mixed_use_within_walking_distance", #SIG
            #"psrc.parcel.percent_open_space_within_walking_distance",
            #"psrc.parcel.percent_residential_within_walking_distance",
            #"psrc.parcel.percent_high_income_households_within_walking_distance", #SIG
            #"psrc.parcel.percent_low_income_households_within_walking_distance", #SIG
            #"psrc.parcel.percent_mid_income_households_within_walking_distance", #SIG
            #"psrc.parcel.percent_minority_households_within_walking_distance", #SIG
            #"psrc.parcel.percent_not_minority_households_within_walking_distance", #SIG
                
            #"psrc.household_x_parcel.gridcell_housing_density_within_walking_distance_multiply_psrc_household_number_of_persons",
            #"psrc.household_x_parcel.gridcell_housing_density_within_walking_distance_multiply_urbansim_household_is_low_income",
            #"psrc.household_x_parcel.gridcell_housing_density_within_walking_distance_multiply_urbansim_household_is_minority",
            #"psrc.household_x_parcel.gridcell_housing_density_within_walking_distance_multiply_urbansim_household_is_young",
            #"psrc.household_x_parcel.gridcell_average_household_size_within_walking_distance_multiply_psrc_household_number_of_persons",
            #"psrc.household_x_parcel.gridcell_percent_mixed_use_within_walking_distance_multiply_urbansim_household_is_minority",
            #"psrc.household_x_parcel.gridcell_percent_residential_within_walking_distance_multiply_urbansim_household_is_high_income",
            #"psrc.household_x_parcel.gridcell_percent_open_space_within_walking_distance_multiply_urbansim_household_is_high_income",
            #"psrc.household_x_parcel.gridcell_percent_commercial_within_walking_distance_multiply_urbansim_household_is_high_income",
            #"psrc.household_x_parcel.gridcell_percent_industrial_within_walking_distance_multiply_urbansim_household_is_high_income",
            #"psrc.household_x_parcel.gridcell_ln_retail_sector_employment_within_walking_distance_multiply_urbansim_household_has_less_cars_than_workers",
            #"psrc.household_x_parcel.gridcell_ln_service_sector_employment_within_walking_distance_multiply_urbansim_household_has_less_cars_than_workers",
            #"psrc.household_x_parcel.gridcell_ln_total_employment_within_walking_distance_multiply_urbansim_household_has_less_cars_than_workers",
            #"psrc.household_x_parcel.gridcell_percent_high_income_households_within_walking_distance_multiply_urbansim_household_is_high_income",
            #"psrc.household_x_parcel.gridcell_percent_low_income_households_within_walking_distance_multiply_urbansim_household_is_low_income",
            #"psrc.household_x_parcel.gridcell_percent_low_income_households_within_walking_distance_multiply_urbansim_household_is_high_income",
            #"psrc.household_x_parcel.gridcell_percent_minority_households_within_walking_distance_multiply_urbansim_household_is_minority",
            #"psrc.household_x_parcel.gridcell_percent_not_minority_households_within_walking_distance_multiply_urbansim_household_is_not_minority",
            
            #"parcel:trip_weighted_average_time_hbw_from_home_am_drive_alone = disaggregate(psrc.zone.trip_weighted_average_time_hbw_from_home_am_drive_alone)",
            #"parcel:trip_weighted_average_time_hbw_from_home_am_transit_walk = disaggregate(psrc.zone.trip_weighted_average_time_hbw_from_home_am_transit_walk)",
            #"parcel:generalized_cost_weighted_access_to_employment_hbw_am_drive_alone = disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone)",
            #"psrc.parcel.travel_time_hbw_am_drive_alone_to_cbd",

            #"psrc.household_x_parcel.worker1_travel_time_hbw_am_drive_alone_from_home_to_work",
            #"psrc.household_x_parcel.worker1_am_total_transit_time_walk_from_home_to_work",
            #"psrc.household_x_parcel.worker2_travel_time_hbw_am_drive_alone_from_home_to_work",
            #"psrc.household_x_parcel.worker2_am_total_transit_time_walk_from_home_to_work",
                
            #"psrc.household_x_parcel.worker1_travel_time_hbw_am_drive_alone_from_home_to_work_if_worker_does_not_use_transit",
            #"psrc.household_x_parcel.worker1_am_total_transit_time_walk_from_home_to_work_if_worker_uses_transit",
            #"psrc.household_x_parcel.worker2_travel_time_hbw_am_drive_alone_from_home_to_work_if_worker_does_not_use_transit",
            #"psrc.household_x_parcel.worker2_am_total_transit_time_walk_from_home_to_work_if_worker_uses_transit",

            #"psrc.household_x_parcel.worker1_am_total_transit_time_walk_from_home_to_work_if_household_has_less_cars_than_nonhome_based_workers",
            #"psrc.household_x_parcel.worker2_am_total_transit_time_walk_from_home_to_work_if_household_has_less_cars_than_nonhome_based_workers",

            #"transit_accessibility.household_x_parcel.worker1_travel_time_hbw_transit_from_work_to_home",
            #"transit_accessibility.household_x_parcel.worker2_travel_time_hbw_transit_from_work_to_home",
            #"transit_accessibility.household_x_parcel.worker1_travel_time_hbw_transit_from_work_to_home_if_worker_uses_transit",
            #"transit_accessibility.household_x_parcel.worker2_travel_time_hbw_transit_from_work_to_home_if_worker_uses_transit",
            ]
            """:""""""
    }
