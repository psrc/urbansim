# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
           "building_type_id = household.disaggregate(building.building_type_id)",
           "large_area_id = household.disaggregate(faz.large_area_id, intermediates=[zone,parcel,building])",
           "age_of_oldest_child = household.aggregate((person.age<=18) * person.age, function=maximum)",
           "age_of_oldest_child_in_private_school = household.aggregate(psrc_parcel.person.is_in_private_k12_school * person.age, function=maximum)",
           "age_of_oldest_child_in_home_school = household.aggregate(psrc_parcel.person.is_in_home_school * person.age, function=maximum)",
           ]
