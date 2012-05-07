# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
   "avg_price_per_unit_in_submarket = safe_array_divide(submarket.aggregate(building.improvement_value),submarket.aggregate(building.residential_units))",
   "avg_price_per_unit_in_district = submarket.disaggregate(district.aggregate(honolulu_parcel.submarket.avg_price_per_unit_in_submarket, function=sum)/district.number_of_agents(submarket))",
   "district_id = submarket.disaggregate(zone.council_district_id)"
           ]