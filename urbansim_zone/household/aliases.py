# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE
aliases = [
        "building_type_id = household.disaggregate(building.building_type_id)",
        "zone_id = household.disaggregate(building.zone_id)",
        "lifestyle = 1 * (household.family_type == 2) * (household.children == 0) + " + \
                     "2 * (household.family_type == 2) * (household.children == 1) * (household.ownrent==1) + " +  \
                     "3 * (household.family_type == 2) * (household.children == 1) * (household.ownrent==2) + " + \
                     "4 * (household.family_type == 1)",
        "lifestylev = 5 * (household.vehicles == 0) + (urbansim_zone.household.lifestyle) * (household.vehicles > 0)"
           ]

