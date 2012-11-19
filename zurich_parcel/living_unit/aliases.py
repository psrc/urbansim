# Opus/UrbanSim urban simulation software.
# Copyright (C) 2012 ETH Zurich, Switzerland
# See opus_core/LICENSE 

aliases = [
           "living_unit_year_built = living_unit.disaggregate(building.year_built)",
           "has_valid_year_built = living_unit.disaggregate(urbansim_parcel.building.has_valid_year_built)",

           ]