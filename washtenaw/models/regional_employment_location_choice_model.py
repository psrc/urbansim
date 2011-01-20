# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import arange, zeros, logical_and, where
from opus_core.logger import logger
from opus_core.misc import unique
from urbansim.models.employment_location_choice_model import EmploymentLocationChoiceModel

class RegionalEmploymentLocationChoiceModel(EmploymentLocationChoiceModel):
    """Run the urbansim ELCM separately for each large area."""
    model_name = "Regional Employment Location Choice Model" 
    large_area_id_name = "large_area_id"
    
    def run(self, specification, coefficients, agent_set, agents_index=None, **kwargs):
        if agents_index is None:
            agents_index = arange(agent_set.size())
        large_areas = agent_set.get_attribute(self.large_area_id_name)
        self.choice_set.compute_variables(["washtenaw.%s.%s" % (self.choice_set.get_dataset_name(), self.large_area_id_name)],
                                                  dataset_pool=self.dataset_pool)
        valid_large_area = where(large_areas[agents_index] > 0)[0]
        if valid_large_area.size > 0:
            unique_large_areas = unique(large_areas[agents_index][valid_large_area])
            cond_array = zeros(agent_set.size(), dtype="bool8")
            cond_array[agents_index[valid_large_area]] = True
            for area in unique_large_areas:
                new_index = where(logical_and(cond_array, large_areas == area))[0]
                self.filter = "%s.%s == %s" % (self.choice_set.get_dataset_name(), self.large_area_id_name, area)
                logger.log_status("ELCM for area %s" % area)
                EmploymentLocationChoiceModel.run(self, specification, coefficients, agent_set, 
                                                 agents_index=new_index, **kwargs)
        agent_index_no_large_area = agents_index[ large_areas[agents_index] <= 0 ]
        if agent_index_no_large_area.size > 0: # run the ELCM for jobs that don't have assigned large_area
            self.filter = None
            logger.log_status("ELCM for jobs with no area assigned")
            choices = EmploymentLocationChoiceModel.run(self, specification, coefficients, agent_set, 
                                                        agents_index=agent_index_no_large_area, **kwargs)
            where_valid_choice = where(choices > 0)[0]
            choices_index = self.choice_set.get_id_index(choices[where_valid_choice])
            chosen_large_areas = self.choice_set.get_attribute_by_index(self.large_area_id_name, choices_index)
            agent_set.modify_attribute(name=self.large_area_id_name, data=chosen_large_areas, 
                                       index=agent_index_no_large_area[where_valid_choice])
