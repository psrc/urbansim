# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import arange, zeros, logical_and, where
from opus_core.logger import logger
from opus_core.misc import unique
from urbansim.models.employment_location_choice_model import EmploymentLocationChoiceModel

class SubareaEmploymentLocationChoiceModel(EmploymentLocationChoiceModel):
    """Run the urbansim ELCM separately for each subarea."""
    model_name = "Subarea Employment Location Choice Model" 

    def __init__(self, group_member, location_set, subarea_id_name, **kwargs):
        super(SubareaEmploymentLocationChoiceModel, self).__init__(group_member, location_set, **kwargs)
        self.subarea_id_name = subarea_id_name
    
    def run(self, specification, coefficients, agent_set, agents_index=None, agents_filter=None, **kwargs):
        if agents_index is None:
            if agents_filter is None:
                agents_index = arange(agent_set.size())
            else:
                agents_index = where(agent_set.compute_variables(agents_filter))[0]

        if self.location_id_string is not None:
            agent_set.compute_variables(self.location_id_string, dataset_pool=self.dataset_pool)
        if not self.subarea_id_name in agent_set.get_attribute_names():
            agent_set.compute_one_variable_with_unknown_package(variable_name="%s" % (self.subarea_id_name), dataset_pool=self.dataset_pool)
        regions = agent_set.get_attribute(self.subarea_id_name)
        self.choice_set.compute_one_variable_with_unknown_package(variable_name="%s" % (self.subarea_id_name), dataset_pool=self.dataset_pool)

        valid_region = where(regions[agents_index] > 0)[0]
        if valid_region.size > 0:
            unique_regions = unique(regions[agents_index][valid_region])
            cond_array = zeros(agent_set.size(), dtype="bool8")
            cond_array[agents_index[valid_region]] = True
            for area in unique_regions:
                new_index = where(logical_and(cond_array, regions == area))[0]
                self.filter = "%s.%s == %s" % (self.choice_set.get_dataset_name(), self.subarea_id_name, area)
                logger.log_status("ELCM for area %s" % area)
                EmploymentLocationChoiceModel.run(self, specification, coefficients, agent_set, 
                                                 agents_index=new_index, **kwargs)
        no_region = where(regions[agents_index] <= 0)[0]
        if no_region.size > 0: # run the ELCM for jobs that don't have assigned region
            self.filter = None
            logger.log_status("ELCM for jobs with no area assigned")
            choices = EmploymentLocationChoiceModel.run(self, specification, coefficients, agent_set, 
                                                 agents_index=agents_index[no_region], **kwargs)
            where_valid_choice = where(choices > 0)[0]
            choices_index = self.choice_set.get_id_index(choices[where_valid_choice])
            chosen_regions = self.choice_set.get_attribute_by_index(self.subarea_id_name, choices_index)
            agent_set.modify_attribute(name=self.subarea_id_name, data=chosen_regions, 
                                       index=no_region[where_valid_choice])
