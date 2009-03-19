# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from numpy import arange, zeros, logical_and, where
from opus_core.logger import logger
from opus_core.misc import unique_values
from urbansim.models.scaling_jobs_model import ScalingJobsModel


class RegionalScalingJobsModel(ScalingJobsModel):
    """Run the urbansim ScalingJobsModel separately for each large area."""
    model_name = "Regional Scaling Jobs Model" 
    large_area_id_name = "large_area_id"
    
    def run(self, location_set, agent_set, agents_index=None, data_objects=None, **kwargs):
        if agents_index is None:
            agents_index = arange(agent_set.size())
        large_areas = agent_set.get_attribute(self.large_area_id_name)
        location_large_area = location_set.compute_variables(["washtenaw.%s.%s" % (location_set.get_dataset_name(), self.large_area_id_name)],
                                                  dataset_pool=self.dataset_pool)
        valid_large_area = where(large_areas[agents_index] > 0)[0]
        if valid_large_area.size > 0:
            unique_large_areas = unique_values(large_areas[agents_index][valid_large_area])
            cond_array = zeros(agent_set.size(), dtype="bool8")
            cond_array[agents_index[valid_large_area]] = True
            for area in unique_large_areas:
                new_index = where(logical_and(cond_array, large_areas == area))[0]
                self.filter = "%s.%s == %s" % (location_set.get_dataset_name(), self.large_area_id_name, area)
                logger.log_status("SJM for area %s" % area)
                ScalingJobsModel.run(self, location_set, agent_set, agents_index=new_index, **kwargs)

        no_large_area = where(large_areas[agents_index] <= 0)[0]
        if no_large_area.size > 0: # run the model for jobs that don't have assigned large_area
            self.filter = None
            logger.log_status("SJM for jobs with no area assigned")
            choices = ScalingJobsModel.run(self, location_set, agent_set, agents_index=agents_index[no_large_area], **kwargs)
            where_valid_choice = where(choices > 0)[0]
            choices_index = location_set.get_id_index(choices[where_valid_choice])
            chosen_large_areas = location_set.get_attribute_by_index(self.large_area_id_name, choices_index)
            agent_set.modify_attribute(name=self.large_area_id_name, data=chosen_large_areas, 
                                       index=no_large_area[where_valid_choice])