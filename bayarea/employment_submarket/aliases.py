# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
   "leases_absorption = (bayarea.employment_submarket.non_residential_absorption)",
   "non_residential_sqft = employment_submarket.aggregate(building.non_residential_sqft)",
   "occupied_non_residential_sqft = employment_submarket.aggregate(establishment.employees) * employment_submarket.disaggregate(building_sqft_per_employee.building_sqft_per_employee)",
   "vacant_non_residential_sqft = clip_to_zero(bayarea.employment_submarket.non_residential_sqft - bayarea.employment_submarket.occupied_non_residential_sqft)",
   "vacancy_rates = safe_array_divide( bayarea.employment_submarket.vacant_non_residential_sqft, (bayarea.employment_submarket.non_residential_sqft).astype('f') )",
   "county_id = employment_submarket.aggregate(building.disaggregate(parcel.county_id),function=median)", #hack
   "employees=employment_submarket.aggregate(establishment.employees)",
   "establishments=employment_submarket.number_of_agents(establishment)",
   "building_sqft_per_employee=employment_submarket.disaggregate(building_sqft_per_employee.building_sqft_per_employee)",
   "total_job_spaces = safe_array_divide(bayarea.employment_submarket.non_residential_sqft, bayarea.employment_submarket.building_sqft_per_employee)",
   "vacant_job_spaces = clip_to_zero(bayarea.employment_submarket.total_job_spaces - bayarea.employment_submarket.employees)",
           ]
