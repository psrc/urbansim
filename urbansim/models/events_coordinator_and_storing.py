#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 

from urbansim.models.events_coordinator import EventsCoordinator
from opus_core.datasets.dataset import DatasetSubset
from opus_core.store.attribute_cache import AttributeCache

class EventsCoordinatorAndStoring(EventsCoordinator):
    def run(self, model_configuration, location_set, development_event_set, *args, **kwargs):
        changed_indices, processed_development_event_indices = \
                        EventsCoordinator.run(self, model_configuration, location_set, 
                                               development_event_set, *args, **kwargs)
        if development_event_set is not None:
            subset = DatasetSubset(development_event_set, processed_development_event_indices)
            subset.write_dataset(out_storage=AttributeCache())
        return (changed_indices, processed_development_event_indices)                               