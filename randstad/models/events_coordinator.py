# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import array, logical_and, logical_or, zeros, where, arange, ones
from urbansim.models.events_coordinator_and_storing import EventsCoordinatorAndStoring
from opus_core.misc import unique
from opus_core.model import Model
from opus_core.logger import logger

class EventsCoordinator(EventsCoordinatorAndStoring):
    """Update the location_set to reflect the changes after the development_event_set.

    TODO: At the moment, the event coordinator assumes that *all* development events have
    the same type_of_change for all attributes, for all events.  This restriction will
    change once we replace the development_events and development_event_history tables with
    the new gridcell_changes, job_changes, and development_constraint_changes tables.
    """

    model_name = "events_coordinator"

    def _set_development_types_for_sqft_and_units(self, location_set, development_type_set, index=None):
         """
         """
         pass
         #events_grid_id = development_event_set.get_attribute("grid_id")
         #events_devtype = development_event_set.get_attribute("development_type_id")
         #events_index_in_location_set = location_set.get_id_index(events_grid_id)
         #location_set.set_values_of_one_attribute("development_type_id", events_devtype,
                                                  #index=events_index_in_location_set)

    def run(self, model_configuration, location_set, development_event_set, *args, **kwargs):
        changed_indices, processed_development_event_indices = \
                        EventsCoordinatorAndStoring.run(self, model_configuration, location_set,
                                               development_event_set, *args, **kwargs)
        if changed_indices.size:
            location_set.set_values_of_one_attribute('year_built', kwargs['current_year']*ones(processed_development_event_indices.size, dtype="int32"),
                                                 index = changed_indices)
            location_set.set_values_of_one_attribute('development_type_id',
                                                     development_event_set.get_attribute('development_type_id')[processed_development_event_indices],
                                                     index = changed_indices)

        return (changed_indices, processed_development_event_indices)
