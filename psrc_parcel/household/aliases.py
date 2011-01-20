# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
           "building_type_id = household.disaggregate(building.building_type_id)",
           "large_area_id = household.disaggregate(faz.large_area_id, intermediates=[zone,parcel,building])",
           ]
