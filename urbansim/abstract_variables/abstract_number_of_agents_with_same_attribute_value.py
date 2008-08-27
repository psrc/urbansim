#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

from opus_core.variables.variable import Variable
from opus_core.variables.variable_name import VariableName
from numpy import where, repeat, ones, float32, resize, array
from numpy import ma, zeros, unique
from urbansim.functions import attribute_label
from opus_core.logger import logger

class abstract_number_of_agents_with_same_attribute_value(Variable):
    """abstract variable for interaction variables that given counts of agents 
    having the same attribute value with the agent at interest, e.g. 
    job_x_building.number_of_jobs_with_same_sector_id_within_walking_distance
    """

    _return_type="int32"
    
    agent_attribute_name = 'to_be_defined_in_fully_qualified_name'
    agent_dependencies = []  # e.g. ['urbansim_parcel.job.grid_id'], can be empty string
    choice_set_dependencies = []  # e.g. ['urbansim_parcel.job.grid_id'], can be empty string
    #agent_attribute_unique_values = []  ##optional, specifying unique values in agent_attribute_name
    geography_dataset_name = 'to_be_defined'
    ## TODO: this expression must have an alias with pattern agents_of_attribute_%(agent_attribute_value)s
    ## once Alan finishes refactoring opus expression to allow function definition, this can be simplied
    expression_agents_of_attribute_by_geography = "'agents_of_attribute_%(agent_attribute_value)s = %(geography_dataset_name)s.aggregate(%(agent_attribute_name)s==%(agent_attribute_value)s)'"
    
    ## this doesn't need to be change
    expression_agents_of_attribute = "'agents_of_attribute_%(agent_attribute_value)s = %(choice_set_name)s.disaggregate(%(geography_dataset_name)s.agents_of_attribute_%(agent_attribute_value)s)'"
                           
    def dependencies(self):
        return [self.agent_attribute_name] + self.agent_dependencies + self.choice_set_dependencies

    def compute(self, dataset_pool):
        interaction_dataset = self.get_dataset()
        choice_set_name = interaction_dataset.get_dataset(2).get_dataset_name()
        agent_category_attr = interaction_dataset.get_dataset(1).get_attribute_by_index(self.agent_attribute_name,
                                                                      interaction_dataset.get_2d_index_of_dataset1())
        if not hasattr(self, 'agent_attribute_unique_values') or self.agent_attribute_unique_values is None or len(self.agent_attribute_unique_values)==0:
            self.agent_attribute_unique_values = unique(agent_category_attr)
            
        agents_of_attribute_by_geography = [ eval( self.expression_agents_of_attribute_by_geography % 
                                                     {'agent_attribute_name':self.agent_attribute_name, 
                                                      'agent_attribute_value':i, 
                                                      'geography_dataset_name':self.geography_dataset_name,
                                                      'choice_set_name': choice_set_name
                                                      } ) 
                                                     for i in self.agent_attribute_unique_values ]        
        self.add_and_solve_dependencies(agents_of_attribute_by_geography, dataset_pool)

        agents_of_attribute = [eval( self.expression_agents_of_attribute % 
                                     {'agent_attribute_name':self.agent_attribute_name, 
                                      'agent_attribute_value':i, 
                                      'geography_dataset_name':self.geography_dataset_name,
                                      'choice_set_name': choice_set_name
                                      } )
                               for i in self.agent_attribute_unique_values]
        self.add_and_solve_dependencies(agents_of_attribute, dataset_pool)

        assert agent_category_attr.min() >= 0
        results = zeros(agent_category_attr.shape, dtype=self._return_type)
        choices = [results] * ( self.agent_attribute_unique_values.max() + 1 )
        for i in self.agent_attribute_unique_values:
            choices[i] = interaction_dataset.get_2d_dataset_attribute("agents_of_attribute_%s" % i)

        results = agent_category_attr.choose(choices)
        
        return results
