# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE
 
from opus_core.upc_sequence import upc_sequence
from opus_core.model_component_creator import ModelComponentCreator

class UPCFactory(ModelComponentCreator):
    def get_model(self, utilities="opus_core.linear_utilities", 
                   probabilities="opus_core.mnl_probabilities",
                   choices="opus_core.random_choices", debuglevel=0):
            
        utilities_class = self.get_model_component(utilities, debuglevel=debuglevel)
        probabilities_class = self.get_model_component(probabilities, debuglevel=debuglevel)
        choices_class = self.get_model_component(choices, debuglevel=debuglevel)
        return upc_sequence(utility_class=utilities_class, probability_class=probabilities_class, 
            choice_class=choices_class, debuglevel=debuglevel)