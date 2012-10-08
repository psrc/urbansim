# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
   "avg_price_per_unit_in_esubmarket = safe_array_divide(employment_submarket.aggregate(building.improvement_value),employment_submarket.aggregate(building.non_residential_sqft))",
   "avg_price_per_unit_in_district = employment_submarket.disaggregate(district.aggregate(honolulu_parcel.employment_submarket.avg_price_per_unit_in_esubmarket, function=sum)/district.number_of_agents(employment_submarket))",
   "district_id = employment_submarket.disaggregate(zone.council_district_id)",
   "is_multi_family_residential = (employment_submarket.building_type_id>2)*(employment_submarket.building_type_id<5)",
   "nonres_building_sqft=employment_submarket.aggregate(building.non_residential_sqft)"
           ]