# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
    "building_type_id=residential_unit.disaggregate(building.building_type_id)",
    "residential_building_type=1*(bayarea.residential_unit.building_type_id==1) + 2*(bayarea.residential_unit.building_type_id==2) + 3*(bayarea.residential_unit.building_type_id==3) + 4*(bayarea.residential_unit.building_type_id>3)",
]

