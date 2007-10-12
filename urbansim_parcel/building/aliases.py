#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 

# this is a test of the expression alias file
# one of the aliases uses a primary attribute in the expression, the other a variable

aliases = [
#   "generic_unit_name = building.disaggregate(generic_building_type.unit_name, intermediates=[building_type])",
   "unit_name = building.disaggregate(building_type.unit_name)",
   "generic_building_type_id = building.disaggregate(building_type.generic_building_type_id)",
   "parcel_sqft = building.disaggregate(parcel.parcel_sqft)",
   "number_of_jobs = building.number_of_agents(job)",
   "occupied_building_sqft_by_non_home_based_jobs = building.aggregate(urbansim_parcel.job.sqft_imputed * urbansim.job.is_building_type_non_home_based)",
   "building_type_name = building.disaggregate(building_type.building_type_name)",
   "is_residential = building.disaggregate(building_type.is_residential)",
   "are_units_building_sqft = building.non_residential_sqft > 0",
   "parcel_sqft_per_unit=safe_array_divide(building.disaggregate(parcel.parcel_sqft),building.residential_units)",
   "building_sqft_per_unit=safe_array_divide(urbansim_parcel.building.building_sqft,building.residential_units)",
   "unit_price = building.disaggregate(urbansim_parcel.parcel.unit_price)",
   "zone_id = building.disaggregate(parcel.zone_id)",
   "has_vacant_residential_units = urbansim_parcel.building.vacant_residential_units > 0"
           ]