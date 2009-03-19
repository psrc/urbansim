# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

aliases = [
           "is_condo_residential=building.disaggregate(building_type.building_type_name=='condo_residential')",
           "is_single_family_residential=building.disaggregate(building_type.building_type_name == 'single_family_residential')",
           "is_multi_family_residential=building.disaggregate(building_type.building_type_name =='multi_family_residential')",
           "is_mobile_home=building.disaggregate(building_type.building_type_name=='mobile_home')",
           "is_commercial=building.disaggregate(building_type.building_type_name =='commercial')",
           "is_industrial=building.disaggregate(building_type.building_type_name =='industrial')",
           "is_office=building.disaggregate(building_type.building_type_name =='office')",
           "is_mixed_use=building.disaggregate(building_type.building_type_name =='mixed_use')",
           "parcel_sqft_per_unit=safe_array_divide(building.disaggregate(parcel.parcel_sqft),building.residential_units)",
           ]