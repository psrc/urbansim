# Opus/UrbanSim urban simulation software.
# Copyright (C) 2012 ETH Zurich, Switzerland
# See opus_core/LICENSE 



aliases = [
           "building_cost = building.improvement_value",
           "sc_total_spaces_0 = sc_number_of_living_units",
           "sc_total_spaces_1 = building.sqm_sector1",
           "sc_total_spaces_2 = building.sqm_sector2",
           "sc_total_spaces_3 = building.sqm_sector3",
           "sc_total_spaces_4 = building.sqm_sector4",
           "sc_total_spaces_5 = building.sqm_sector5",
           "sc_total_spaces_6 = building.sqm_sector6",
           "sc_total_spaces_7 = building.sqm_sector7",
           "sc_total_spaces_8 = building.sqm_sector8",
           "sc_total_spaces_99 = building.sqm_sector99",
           "s1 = urbansim_parcel.building.number_of_jobs_of_sector_1 * 50",
           "s2 = urbansim_parcel.building.number_of_jobs_of_sector_2 * 35",
           "s3 = urbansim_parcel.building.number_of_jobs_of_sector_3 * 55",
           "s4 = urbansim_parcel.building.number_of_jobs_of_sector_4 * 60",
           "s5 = urbansim_parcel.building.number_of_jobs_of_sector_5 * 80",
           "s6 = urbansim_parcel.building.number_of_jobs_of_sector_6 * 35",
           "s7 = urbansim_parcel.building.number_of_jobs_of_sector_7 * 35",
           "s8 = urbansim_parcel.building.number_of_jobs_of_sector_8 * 45",
           "s49 = urbansim_parcel.building.number_of_jobs_of_sector_49 * 50",
           "s99 = urbansim_parcel.building.number_of_jobs_of_sector_99 * 100",
           "occupied_non_residential_spaces = zurich_parcel.building.s1 + zurich_parcel.building.s2 + zurich_parcel.building.s3+ zurich_parcel.building.s4 + zurich_parcel.building.s5 + zurich_parcel.building.s6 + zurich_parcel.building.s7 + zurich_parcel.building.s8 + zurich_parcel.building.s49 + zurich_parcel.building.s99",
           "occupied_residential_units = numpy.minimum(building.number_of_agents(household), building.number_of_agents(living_unit))",
           "sc_occupied_spaces_0 = zurich_parcel.building.occupied_residential_units",
           "sc_occupied_spaces_1 = urbansim_parcel.building.number_of_jobs_of_sector_1 * 50",
           "sc_occupied_spaces_2 = urbansim_parcel.building.number_of_jobs_of_sector_2 * 35",
           "sc_occupied_spaces_3 = urbansim_parcel.building.number_of_jobs_of_sector_3 * 55",
           "sc_occupied_spaces_4 = urbansim_parcel.building.number_of_jobs_of_sector_4 * 60",
           "sc_occupied_spaces_5 = urbansim_parcel.building.number_of_jobs_of_sector_5 * 80",
           "sc_occupied_spaces_6 = urbansim_parcel.building.number_of_jobs_of_sector_6 * 35",
           "sc_occupied_spaces_7 = urbansim_parcel.building.number_of_jobs_of_sector_7 * 35",
           "sc_occupied_spaces_8 = urbansim_parcel.building.number_of_jobs_of_sector_8 * 45",
           "sc_occupied_spaces_99 = urbansim_parcel.building.number_of_jobs_of_sector_99 * 100",
           "building_test = building.land_area",
           ]