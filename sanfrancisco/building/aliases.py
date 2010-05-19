# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
       "activity_constraint = building.disaggregate(parcel.activity_constraint)",
       "building_class_id=building.disaggregate(building_type_classification.class_id, intermediates=[building_type])",
       "building_class_name=building.disaggregate(building_type_classification.name, intermediates=[building_type])",
       "building_sqft_per_unit=safe_array_divide(building.building_sqft, building.residential_units)",
       "employment = building.aggregate(business.employment)",
       "is_residential = building.disaggregate(building_type_classification.is_residential, intermediates=[building_type])",            
       "number_of_businesses=building.number_of_agents(business)",
       "number_of_households=building.number_of_agents(household)",
       "population=building.aggregate(sanfrancisco.household.persons)",
       "occupied_sqft = numpy.clip(building.aggregate(business.sqft), 0, building.non_residential_sqft)",      
       "sum_business_sqft = building.aggregate(business.sqft)",
       "unit_name = building.disaggregate(sanfrancisco.building_type.unit_name)",
       "unit_capacity_name = building.disaggregate(sanfrancisco.building_type.unit_capacity_name)",
       "vacant_building_sqft=clip_to_zero(sanfrancisco.building.building_sqft - sanfrancisco.building.occupied_sqft)",
       "vacant_building_sqft_without_clip=sanfrancisco.building.building_sqft - sanfrancisco.building.occupied_sqft",
       "vacant_non_residential_building_sqft=clip_to_zero(building.non_residential_building_sqft - sanfrancisco.building.occupied_sqft)",
       "vacant_non_residential_sqft_without_clip=building.building.non_residential_sqft - sanfrancisco.building.occupied_sqft",
       "vacant_residential_units=clip_to_zero(sanfrancisco.building.residential_units - sanfrancisco.building.number_of_households)",
       "vacant_residential_units_without_clip=sanfrancisco.building.residential_units - sanfrancisco.building.number_of_households",
       "zone_id=building.disaggregate(parcel.zone_id)",
           ]
