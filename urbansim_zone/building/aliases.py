# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE
aliases = [
        "total_residential_units = building.sf_residential_units + mf_residential_units",
        "number_of_households = building.number_of_agents(household)",
        "vacant_residential_units = clip_to_zero(urbansim_zone.building.total_residential_units - urbansim_zone.building.number_of_households)",
        
           ]
