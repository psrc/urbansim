# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE
aliases = [
        "number_of_households = building.number_of_agents(household)",
        "vacant_residential_units = clip_to_zero(building.residential_units - urbansim_zone.building.number_of_households)",
           ]
