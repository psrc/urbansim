# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
   "county_id = submarket.aggregate(building.disaggregate(parcel.county_id),function=median)",
   "residential_units = submarket.aggregate(building.residential_units)",
   "households = submarket.number_of_agents(household)",
   "sales_absorption = (drcog.submarket.residential_absorption)", # * (submarket.tenure_id==1)",
   "rent_absorption = (drcog.submarket.residential_absorption)", #  * (submarket.tenure_id==2)",
   "residential_units = submarket.aggregate(building.residential_units)",
   "vacant_residential_units = clip_to_zero(drcog.submarket.residential_units - drcog.submarket.households)",
   "vacancy_rates = safe_array_divide( drcog.submarket.vacant_residential_units, (drcog.submarket.residential_units).astype('f') )",
           ]
