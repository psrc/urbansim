#
# Opus software. Copyright (C) 2005-2008 University of Washington
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