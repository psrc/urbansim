# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
       "is_residential = development_event_history.disaggregate(building_type_classification.is_residential, intermediates=[building_type])",
       "building_class_id = development_event_history.disaggregrate(building_type.class_id)",
       "occupied_mixed_spaces = sanfrancisco.development_event_history.occupied_sqft + safe_array_divide(sanfrancisco.building.number_of_households, (building.residential_units).astype('float')) * building.residential_sqft",
       "total_mixed_spaces = development_event_history.non_residential_sqft + building.residential_sqft",   
       "building_group_id=development_event_history.disaggregate(building_type_classification.grouping_id, intermediates=[building_type])",
       ]