# Opus/UrbanSim urban simulation software.
# Copyright (C) 2012 ETH Zurich, Switzerland
# See opus_core/LICENSE 



aliases = [
           "building_cost = building.improvement_value",
           "sc_total_spaces_1 = building.residential_units",
           "sc_total_spaces_0 = building.non_residential_sqft",
           "s1 = urbansim_parcel.building.number_of_jobs_of_sector_1 * 50",
           "s2 = urbansim_parcel.building.number_of_jobs_of_sector_2 * 100",
           "s3 = urbansim_parcel.building.number_of_jobs_of_sector_3 * 50",
           "s4 = urbansim_parcel.building.number_of_jobs_of_sector_4 * 50",
           "s5 = urbansim_parcel.building.number_of_jobs_of_sector_5 * 100",
           "s6 = urbansim_parcel.building.number_of_jobs_of_sector_6 * 50",
           "s7 = urbansim_parcel.building.number_of_jobs_of_sector_7 * 15",
           "s8 = urbansim_parcel.building.number_of_jobs_of_sector_8 * 25",
           "s49 = urbansim_parcel.building.number_of_jobs_of_sector_49 * 50",
           "s99 = urbansim_parcel.building.number_of_jobs_of_sector_99 * 100",
           "occupied_non_residential_spaces = zurich_parcel.building.s1 + zurich_parcel.building.s2 + zurich_parcel.building.s3+ zurich_parcel.building.s4 + zurich_parcel.building.s5 + zurich_parcel.building.s6 + zurich_parcel.building.s7 + zurich_parcel.building.s8 + zurich_parcel.building.s49 + zurich_parcel.building.s99",
           "occupied_residential_units = numpy.minimum(building.number_of_agents(household), building.number_of_agents(living_unit))",
           "sc_occupied_spaces_1 = zurich_parcel.building.occupied_residential_units",
           "sc_occupied_spaces_0 = zurich_parcel.building.occupied_non_residential_spaces",
           "building_test = building.land_area",
           ]