# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.variables.variable_name import VariableName
from numpy import where, repeat, ones, float32, resize, array
from numpy import ma, zeros, arange, logical_and, searchsorted
from opus_core.misc import unique
from urbansim.functions import attribute_label
from opus_core.logger import logger
from opus_core import ndimage

class abstract_frequency_by_category(Variable):
    """abstract variable for interaction variables that given counts of agents 
    by agent and choice set category
    """

    _return_type="int32"
    
    agent_filter_attribute = None        # 'to_be_defined_in_fully_qualified_name'    
    category_inflating_factor  = 10
    agent_category_definition = []   # e.g. ['urbansim_parcel.job.grid_id'], can be empty string
    choice_category_definition = []  # e.g. ['urbansim_parcel.job.grid_id'], can be empty string
    
    def dependencies(self):
        if self.agent_filter_attribute is None or len(self.agent_filter_attribute) == 0:
            return self.agent_category_definition + self.choice_category_definition
        return [self.agent_filter_attribute] + self.agent_category_definition + self.choice_category_definition

    def compute(self, dataset_pool):
        """##TODO: add docstring
        """
        interaction_set = self.get_dataset()
        agent_set = interaction_set.get_dataset(1)
        choice_set = interaction_set.get_dataset(2)
        #agent_set.compute_variables(self.agent_category_definition)
        #choice_set.compute_variables(self.choice_category_definition)
        frequency, unique_agent_category_id, unique_choice_category_id, agent_category_id, choice_category_id = \
                get_category_and_frequency(agent_set, self.agent_category_definition,
                                           choice_set, self.choice_category_definition,
                                           self.agent_filter_attribute, self.category_inflating_factor,
                                           dataset_pool)

        agent_index_to_agent_category = searchsorted(unique_agent_category_id, agent_category_id[interaction_set.get_2d_index_of_dataset1()])
        choice_index_to_choice_category = searchsorted(unique_choice_category_id, choice_category_id[interaction_set.get_2d_index()])

        return frequency[agent_index_to_agent_category, choice_index_to_choice_category]

def get_category_and_frequency(agent_set, agent_category_definition,
                               choice_set, choice_category_definition,
                               agent_filter_attribute, category_inflating_factor,
                               dataset_pool):

    agent_category_variable = []
    for i in range( len(agent_category_definition) ):
        agent_category_variable.append( VariableName(agent_category_definition[i]).get_alias() + \
                '*%i' % category_inflating_factor**i )
    if len(agent_category_variable) > 0:
        agent_category_id = agent_set.compute_variables("agent_category_id=" + ' + '.join(agent_category_variable), dataset_pool=dataset_pool)
    else:
        agent_category_id = agent_set.get_id_attribute()
    unique_agent_category_id = unique(agent_category_id)

    choice_category_variable = []
    for i in range( len(choice_category_definition) ):
        #choice_category_variable.append( VariableName(choice_category_definition[i]).get_alias() + \
                #        '*%i' % category_inflating_factor**i )
        choice_category_variable.append( choice_category_definition[i] + \
                '*%i' % category_inflating_factor**i )
    if len(choice_category_variable) > 0:
        choice_category_id = choice_set.compute_variables("choice_category_id=" + ' + '.join( choice_category_variable), dataset_pool=dataset_pool)
        agent_choice_category_id = agent_set.compute_variables('choice_category_id=%s.disaggregate(%s.choice_category_id)' % \
                                                               (agent_set.get_dataset_name(), choice_set.get_dataset_name()),
                                                               dataset_pool=dataset_pool)
    else:
        choice_category_id = choice_set.get_id_attribute()
        agent_choice_category_id = agent_set.get_attribute(choice_set.get_id_name()[0])

    unique_choice_category_id = unique(choice_category_id)

    if agent_filter_attribute is not None and len(agent_filter_attribute) > 0:
        agent_filter = agent_set.compute_variables(agent_filter_attribute, dataset_pool=dataset_pool)
    else:
        agent_filter = ones(agent_set.size(), dtype='bool')

    frequency = zeros( (unique_agent_category_id.size, unique_choice_category_id.size), dtype="int32" )
    for i in range(unique_agent_category_id.size): # iterate over agent category
        is_agent_of_this_category = logical_and(agent_filter, agent_category_id == unique_agent_category_id[i]).astype("int32")
        frequency[i,:] = ndimage.sum(is_agent_of_this_category, labels=agent_choice_category_id.astype("int32"), index=unique_choice_category_id.astype("int32"))
    return frequency, unique_agent_category_id, unique_choice_category_id, agent_category_id, choice_category_id

