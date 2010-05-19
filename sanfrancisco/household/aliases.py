# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
           "parcel_id=household.disaggregate(building.parcel_id)",
           "zone_id=household.disaggregate(parcel.zone_id, intermediates=[building])",
           "persons=household.number_of_agents(person)",
           ]
