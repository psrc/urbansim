# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
   "avg_rent_per_unit_in_submarket = safe_array_divide(submarket.aggregate(residential_unit.rent,intermediates=[building]),submarket.aggregate(residential_unit.rent>0,intermediates=[building]))",
   "avg_price_per_unit_in_submarket = safe_array_divide(submarket.aggregate(residential_unit.sale_price,intermediates=[building]),submarket.aggregate(residential_unit.sale_price>0,intermediates=[building]))",
   "avg_price_per_unit_in_superdistrict = submarket.disaggregate(superdistrict.aggregate(bayarea.submarket.avg_price_per_unit_in_submarket, function=sum)/superdistrict.number_of_agents(submarket))",
   "avg_price_per_unit_in_county = submarket.disaggregate(county.aggregate(bayarea.submarket.avg_price_per_unit_in_submarket, function=sum)/county.number_of_agents(submarket))",
   "avg_rent_per_unit_in_county = submarket.disaggregate(county.aggregate(bayarea.submarket.avg_rent_per_unit_in_submarket, function=sum)/county.number_of_agents(submarket))",
   "county_id = submarket.aggregate(building.disaggregate(parcel.county_id),function=median)"
           ]