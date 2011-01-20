# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE
from opus_core.interaction_dataset import InteractionDataset
from opus_core.resources import Resources

class LandCoverXChoiceDataset(InteractionDataset):
    """InteractionDataset for the LCCM. Needed for flushing variables."""
    def _compute_if_needed(self, name, dataset_pool, resources=None, **kwargs):
        result = InteractionDataset._compute_if_needed(self, name, dataset_pool, resources, **kwargs)
        if isinstance(resources, Resources) and resources.is_in("flush_variables") and \
            resources["flush_variables"]:
                self.dataset1.flush_dataset()
        return result