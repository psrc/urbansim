# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
   "leases_absorption = (drcog.employment_submarket.non_residential_absorption)",
   "non_residential_sqft = employment_submarket.aggregate(building.non_residential_sqft)",
   "occupied_non_residential_sqft = employment_submarket.aggregate(establishment.employees) * employment_submarket.disaggregate(building_sqft_per_job.building_sqft_per_job)",
   "vacant_non_residential_sqft = clip_to_zero(drcog.employment_submarket.non_residential_sqft - drcog.employment_submarket.occupied_non_residential_sqft)",
   "vacancy_rates = safe_array_divide( drcog.employment_submarket.vacant_non_residential_sqft, (drcog.employment_submarket.non_residential_sqft).astype('f') )",
   "building_sqft_per_employee=employment_submarket.disaggregate(building_sqft_per_job.building_sqft_per_job)",
           ]
