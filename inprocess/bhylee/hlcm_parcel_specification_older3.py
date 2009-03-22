# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

specification = {}

specification = {
        0:   #submodel_id
            [
             "ln_sqft_per_unit = ln(psrc_parcel.building.sqft_per_unit)",
             #"ln_improvement_value = ln(psrc_parcel.building.improvement_value)",
             "ln_land_area = ln(psrc_parcel.building.land_area)",
             "ln_residential_units = ln(psrc_parcel.building.residential_units)",
             "ln_year_built = ln(psrc_parcel.building.year_built)",
            #"ln_number_of_jobs_within_walking_distance = ln(psrc.parcel.number_of_jobs_within_walking_distance)",
            #"ln_residential_units_within_walking_distance = ln(psrc.parcel.residential_units_within_walking_distance)",
            #"square_year_built = parcel.year_built**2",
            
            #"building.disaggregate(psrc.household_x_parcel.income_and_ln_built_sf)",
            #"income_x_ln_sqft_per_unit = household.income * ln_bounded(psrc_parcel.building.sqft_per_unit)",
            #"building.disaggregate(psrc.household_x_parcel.income_and_ln_land_value)",
            "ln_income_less_price_per_unit = ln_bounded(household.income - (urbansim_parcel.building.unit_price/10.)*urbansim_parcel.building.building_sqft)",
            #"income_x_ln_land_value = household.income * building.disaggregate(ln_bounded(parcel.land_value))",
            #"income_x_ln_improvement_value = household.income * ln_bounded(psrc_parcel.building.improvement_value)",
            #"psrc.household_x_parcel.income_and_ln_lot_sf",
            #"psrc.household_x_parcel.income_and_ln_residential_units",
            #"psrc.household_x_parcel.income_and_year_built",
            #"psrc.parcel.is_pre_1940",
            #"psrc.parcel.population_density_in_gridcell",
            #"psrc.parcel.ln_retail_sector_employment_within_walking_distance",
            #"urbansim.household_x_gridcell.income_and_year_built",
            
            #"ln_emp_w15m_drive_alone = parcel.disaggregate(psrc.zone.ln_employment_within_15_minutes_travel_time_hbw_am_drive_alone)",
            #"ln_employment_within_15_minutes_travel_time_hbw_am_transit_walk = parcel.disaggregate(psrc.zone.ln_employment_within_15_minutes_travel_time_hbw_am_transit_walk)",
            #"ln_employment_within_30_minutes_travel_time_hbw_am_drive_alone = parcel.disaggregate(psrc.zone.ln_employment_within_30_minutes_travel_time_hbw_am_drive_alone)",
            #"ln_employment_within_30_minutes_travel_time_hbw_am_transit_walk = parcel.disaggregate(psrc.zone.ln_employment_within_30_minutes_travel_time_hbw_am_transit_walk)",
#            "psrc.parcel.average_household_size_within_walking_distance", #SIG
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
            
            #"trip_weighted_average_time_hbw_from_home_am_drive_alone = parcel.disaggregate(psrc.zone.trip_weighted_average_time_hbw_from_home_am_drive_alone)",
            #"trip_weighted_average_time_hbw_from_home_am_transit_walk = parcel.disaggregate(psrc.zone.trip_weighted_average_time_hbw_from_home_am_transit_walk)",
            #"generalized_cost_weighted_access_to_employment_hbw_am_drive_alone = parcel.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone)",
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
            
            "ln_employment_within_15_minutes_travel_time_hbw_am_drive_alone = parcel.disaggregate(psrc.zone.ln_employment_within_15_minutes_travel_time_hbw_am_drive_alone)",
            #"ln_employment_within_15_minutes_travel_time_hbw_am_transit_walk = parcel.disaggregate(psrc.zone.ln_employment_within_15_minutes_travel_time_hbw_am_transit_walk)",
            #"ln_employment_within_30_minutes_travel_time_hbw_am_drive_alone = parcel.disaggregate(psrc.zone.ln_employment_within_30_minutes_travel_time_hbw_am_drive_alone)",
            #"ln_employment_within_30_minutes_travel_time_hbw_am_transit_walk = parcel.disaggregate(psrc.zone.ln_employment_within_30_minutes_travel_time_hbw_am_transit_walk)",
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
            
            #"trip_weighted_average_time_hbw_from_home_am_drive_alone = parcel.disaggregate(psrc.zone.trip_weighted_average_time_hbw_from_home_am_drive_alone)",
            #"trip_weighted_average_time_hbw_from_home_am_transit_walk = parcel.disaggregate(psrc.zone.trip_weighted_average_time_hbw_from_home_am_transit_walk)",
            #"generalized_cost_weighted_access_to_employment_hbw_am_drive_alone = parcel.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone)",
            #"psrc.parcel.travel_time_hbw_am_drive_alone_to_cbd",

            "psrc.household_x_parcel.worker1_travel_time_hbw_am_drive_alone_from_home_to_work",
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
            
            "ln_employment_within_15_minutes_travel_time_hbw_am_drive_alone = parcel.disaggregate(psrc.zone.ln_employment_within_15_minutes_travel_time_hbw_am_drive_alone)",
            #"ln_employment_within_15_minutes_travel_time_hbw_am_transit_walk = parcel.disaggregate(psrc.zone.ln_employment_within_15_minutes_travel_time_hbw_am_transit_walk)",
            #"ln_employment_within_30_minutes_travel_time_hbw_am_drive_alone = parcel.disaggregate(psrc.zone.ln_employment_within_30_minutes_travel_time_hbw_am_drive_alone)",
            #"ln_employment_within_30_minutes_travel_time_hbw_am_transit_walk = parcel.disaggregate(psrc.zone.ln_employment_within_30_minutes_travel_time_hbw_am_transit_walk)",
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
            
            #"trip_weighted_average_time_hbw_from_home_am_drive_alone = parcel.disaggregate(psrc.zone.trip_weighted_average_time_hbw_from_home_am_drive_alone)",
            #"trip_weighted_average_time_hbw_from_home_am_transit_walk = parcel.disaggregate(psrc.zone.trip_weighted_average_time_hbw_from_home_am_transit_walk)",
            #"generalized_cost_weighted_access_to_employment_hbw_am_drive_alone = parcel.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone)",
            #"psrc.parcel.travel_time_hbw_am_drive_alone_to_cbd",

            "psrc.household_x_parcel.worker1_travel_time_hbw_am_drive_alone_from_home_to_work",
            #"psrc.household_x_parcel.worker1_am_total_transit_time_walk_from_home_to_work",
            "psrc.household_x_parcel.worker2_travel_time_hbw_am_drive_alone_from_home_to_work",
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
