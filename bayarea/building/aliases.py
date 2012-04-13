# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
    "zone_id = building.disaggregate(parcel.zone_id)",
    "superd = building.disaggregate(parcel.superd)",
    "neighborhood_type = building.disaggregate(parcel.neighborhood_type)",
    "building_type = 1*(building.building_type_id==1) + 2*(building.building_type_id==2) + 3*(building.building_type_id>2)",
    "tenure_id = 1*(building.tenure<2) + 2*(building.tenure==2)",
    "building_type_id = building.building_type_id"
           ]
#"building_type = 1*(building.building_type_id==1) + 2*(building.building_type_id==2) + 3*(building.building_type_id>2)"