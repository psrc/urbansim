# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import arange, zeros, logical_and, where
from opus_core.logger import logger
from opus_core.misc import unique
from urbansim_zone.models.development_project_location_choice_model import DevelopmentProjectLocationChoiceModel

class SubareaDevelopmentProjectLocationChoiceModel(DevelopmentProjectLocationChoiceModel):
    """Run DPLCM separately for each subarea."""
    
    model_name = "Subarea Development Project Location Choice Model"
    model_short_name = "SDPLCM"

    def __init__(self, location_set, subarea_id_name, **kwargs):
        DevelopmentProjectLocationChoiceModel.__init__(self, location_set, 
                                                                  **kwargs)
        self.subarea_id_name = subarea_id_name
    
    def run(self, specification, coefficients, agent_set, agents_index=None, 
            flush_after_each_subarea=False, agents_filter=None, **kwargs):
        if agents_index is None:
            if agents_filter is None:
                agents_index = arange(agent_set.size())
            else:
                agents_index = where(agent_set.compute_variables(agents_filter))[0]

        if self.location_id_string is not None:
            agent_set.compute_variables(self.location_id_string, 
                                        dataset_pool=self.dataset_pool)
        if not self.subarea_id_name in agent_set.get_attribute_names():
            agent_set.compute_one_variable_with_unknown_package(variable_name="%s" % (self.subarea_id_name), 
                                                                dataset_pool=self.dataset_pool)
        subareas = agent_set.get_attribute(self.subarea_id_name)        
        self.choice_set.compute_one_variable_with_unknown_package(variable_name="%s" % (self.subarea_id_name), 
                                                                  dataset_pool=self.dataset_pool)
        
        valid_subarea = where(subareas[agents_index] > 0)[0]
        filter0 = self.filter #keep a copy of the original self.filter
        # this loop iterates through unique subareas
        if valid_subarea.size > 0:
            unique_subareas = unique(subareas[agents_index][valid_subarea])
            cond_array = zeros(agent_set.size(), dtype="bool8")
            cond_array[agents_index[valid_subarea]] = True            
            for subarea in unique_subareas:
                new_index = where(logical_and(cond_array, subareas == subarea))[0]
                #append subarea_id filter to the original filter string if it is set
                subarea_filter = "(%s.%s==%s)" % (self.choice_set.get_dataset_name(), self.subarea_id_name, subarea)
                if filter0:
                    self.filter = filter0 + "*" + subarea_filter
                else:
                    self.filter = subarea_filter
                logger.log_status("DPLCM for subarea %s" % subarea)
                DevelopmentProjectLocationChoiceModel.run(self, specification, coefficients, agent_set, 
                                                          agents_index=new_index, **kwargs)
                if flush_after_each_subarea:
                    agent_set.flush_dataset()
                    self.choice_set.flush_dataset()
        self.filter = filter0
        no_subarea = where(subareas[agents_index] <= 0)[0]

        
        # this loop handles agents w/out a subarea
        if no_subarea.size > 0:            
            logger.log_status("DPLCM for agents with no subarea assigned")
            choices = DevelopmentProjectLocationChoiceModel.run(self, specification, coefficients, agent_set, 
                                                                agents_index=agents_index[no_subarea], **kwargs)
            where_valid_choice = where(choices > 0)[0]
            choices_index = self.choice_set.get_id_index(choices[where_valid_choice])
            chosen_subareas = self.choice_set.get_attribute_by_index(self.subarea_id_name, choices_index)
            agent_set.modify_attribute(name=self.subarea_id_name, data=chosen_subareas, 
                                       index=no_subarea[where_valid_choice])

