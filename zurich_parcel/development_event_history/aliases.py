# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
           "is_residential = development_event_history.disaggregate(building_type.is_residential)",
           "sc_total_spaces_0 = development_event_history.number_of_agents(living_units_history)",
           "sc_total_spaces_1 = development_event_history.sqm_sector1",
           "sc_total_spaces_2 = development_event_history.sqm_sector2",
           "sc_total_spaces_3 = development_event_history.sqm_sector3",
           "sc_total_spaces_4 = development_event_history.sqm_sector4",
           "sc_total_spaces_5 = development_event_history.sqm_sector5",
           "sc_total_spaces_6 = development_event_history.sqm_sector6",
           "sc_total_spaces_7 = development_event_history.sqm_sector7",
           "sc_total_spaces_8 = development_event_history.sqm_sector8",
           "sc_total_spaces_99 = development_event_history.sqm_sector99",
           "sc_occupied_spaces = -1 * (development_event_history.building_type_id > 0)", #filled with dummy values; should not be used
           ]
