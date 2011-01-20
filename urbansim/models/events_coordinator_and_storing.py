# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.models.events_coordinator import EventsCoordinator
from opus_core.datasets.dataset import DatasetSubset
from opus_core.store.attribute_cache import AttributeCache

class EventsCoordinatorAndStoring(EventsCoordinator):
    def run(self, location_set, development_event_set, *args, **kwargs):
        changed_indices, processed_development_event_indices = \
                        EventsCoordinator.run(self, location_set, 
                                               development_event_set, *args, **kwargs)
        if development_event_set is not None:
            subset = DatasetSubset(development_event_set, processed_development_event_indices)
            subset.write_dataset(out_storage=AttributeCache())
        return (changed_indices, processed_development_event_indices)                               