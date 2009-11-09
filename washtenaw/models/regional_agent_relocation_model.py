# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import arange, zeros, logical_and, where, array, concatenate
from opus_core.logger import logger
from opus_core.misc import unique_values
from urbansim.models.agent_relocation_model import AgentRelocationModel
from opus_core.datasets.dataset import DatasetSubset

class RegionalAgentRelocationModel(AgentRelocationModel):
    """Run the urbansim ARM separately for each large area."""
    
    large_area_id_name = "large_area_id"
    
    def run(self, agent_set, **kwargs):

        large_areas = agent_set.get_attribute(self.large_area_id_name)
        valid_large_area = where(large_areas > 0)[0]
        if valid_large_area.size > 0:
            unique_large_areas = unique_values(large_areas[valid_large_area])
            cond_array = zeros(agent_set.size(), dtype="bool8")
            cond_array[valid_large_area] = True
            result = array([], dtype="int32")
            for area in unique_large_areas:
                new_index = where(logical_and(cond_array, large_areas == area))[0]
                agent_subset =  DatasetSubset(agent_set, new_index)
                logger.log_status("ARM for area %s (%s agents)" % (area, agent_subset.size()))
                this_result = AgentRelocationModel.run(self, agent_subset, **kwargs)
                result = concatenate((result, new_index[this_result]))
        no_large_area = where(large_areas <= 0)[0]
        result = concatenate((result, no_large_area))
        return result
