# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.models.agent_location_choice_model import AgentLocationChoiceModel
from opus_core.hierarchical_choice_model import HierarchicalChoiceModel

class AgentHierarchicalLocationChoiceModel(AgentLocationChoiceModel, HierarchicalChoiceModel):
    """This model combines the HierarchicalChoiceModel and AgentLocationChoiceModel.
    It can be used for location choice models that require sampling of alternatives.
    """

    def __init__(self, location_set, nested_structure=None, stratum=None, model_name=None, short_name=None,
                        sampler="opus_core.samplers.stratified_sampler", 
                        utilities="opus_core.hierarchical_linear_utilities",
                        probabilities="opus_core.nl_probabilities", **kwargs):
        AgentLocationChoiceModel.__init__(self, location_set=location_set, model_name=model_name, 
                                          short_name=short_name, sampler=sampler, utilities=utilities,
                                          probabilities=probabilities, **kwargs)
        HierarchicalChoiceModel.create_nested_and_tree_structure(self, nested_structure, stratum, **kwargs)
        self.model_interaction = ModelInteractionHierLCM(self, kwargs.get('interaction_pkg',"urbansim"), self.choice_set)

    def run_chunk(self, agents_index, agent_set, specification, coefficients):
        HierarchicalChoiceModel.add_logsum_to_specification(self, specification, coefficients)
        HierarchicalChoiceModel.init_membership_in_nests(self)
        return AgentLocationChoiceModel.run_chunk(self, agents_index, agent_set, specification, coefficients)
        
    def estimate(self, specification, *args, **kwargs):
        HierarchicalChoiceModel.init_membership_in_nests(self)
        HierarchicalChoiceModel.delete_logsum_from_specification(self, specification)
        return AgentLocationChoiceModel.estimate(self, specification, *args, **kwargs)
    
    def estimate_step(self):
        self.set_correct_for_sampling()
        result = AgentLocationChoiceModel.estimate_step(self)
        HierarchicalChoiceModel.add_logsum_to_coefficients(self, result)
        return result

    def set_choice_set_size(self, **kwargs):
        HierarchicalChoiceModel.set_choice_set_size(self, **kwargs)
        
    def get_number_of_elemental_alternatives(self):
        return HierarchicalChoiceModel.get_number_of_elemental_alternatives(self)
        
from opus_core.hierarchical_choice_model import ModelInteractionHM
class ModelInteractionHierLCM(ModelInteractionHM):
    def set_selected_choice_for_LCM(self, selected_choice):
        self.selected_choice = selected_choice