# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
           "is_residential = development_event_history.disaggregate(building_type.is_residential)",
           "SC_total_spaces_1 = building.residential_units",
           "SC_total_spaces_0 = building.non_residential_sqft",
           "SC_occupied_spaces = -1 * (development_event_history.building_type_id > 0)", #filled with dummy values; should not be used
           ]