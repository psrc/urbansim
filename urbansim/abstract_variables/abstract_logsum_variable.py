# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import where, repeat, zeros, ones, float32, resize, array
from numpy import ma, logical_or, logical_not
from urbansim.functions import attribute_label
from opus_core.logger import logger

class abstract_logsum_variable(Variable):
    """abstract variable for interaction logsum variables with car num/income category matched to
    agent's car num/income (agent_category_attribute) """

    default_value = 180.0
    agent_zone_id = 'to_be_defined_in_fully_qualified_name'
    agent_category_attribute = 'to_be_defined_in_fully_qualified_name'    
    location_zone_id = 'to_be_defined_in_fully_qualified_name'
    travel_data_attributes = 'to_be_defined_in_fully_qualified_name'  # a dict {1:'travel_data.logsum_hbw_am_income_1'}
    direction_from_home = True

    def dependencies(self):
        return [ self.agent_zone_id, self.agent_category_attribute, self.location_zone_id] + list(self.travel_data_attributes.values())

    def compute(self, dataset_pool):
        interaction_dataset = self.get_dataset()
        travel_data = dataset_pool.get_dataset('travel_data')

        var1 = interaction_dataset.get_dataset(1).get_attribute_by_index(self.agent_zone_id,
                                                                      interaction_dataset.get_2d_index_of_dataset1())
        var2 = interaction_dataset.get_2d_dataset_attribute(self.location_zone_id)
        if self.direction_from_home:
            home_zone = var1.astype("int32")
            work_zone = var2.astype("int32")
        else:
            home_zone = var2.astype("int32")
            work_zone = var1.astype("int32")
            
        results = resize(array([self.default_value], dtype=float32), home_zone.shape)
        agent_category_attr = interaction_dataset.get_dataset(1).get_attribute_by_index(self.agent_category_attribute,
                                                                      interaction_dataset.get_2d_index_of_dataset1())
        assert agent_category_attr.min() >= 0        
        max_choices = agent_category_attr.max() + 1
        choices = [results] * max_choices
        for i in range(max_choices):
            if i in self.travel_data_attributes:
                travel_data_attr_mat = travel_data.get_attribute_as_matrix(self.travel_data_attributes[i],
                                                                           fill=self.default_value)
                choices[i] = travel_data_attr_mat[home_zone, work_zone]

        results = agent_category_attr.choose(choices)
        
        missing_pairs_index = travel_data.get_od_pair_index_not_in_dataset(home_zone, work_zone)
        if missing_pairs_index[0].size > 0:
            results[missing_pairs_index] = self.default_value
            logger.log_warning("zone pairs at index %s are not in travel data; value set to %s." % ( str(missing_pairs_index), self.default_value) )
        
        has_category = zeros(home_zone.shape, dtype='bool')
        for k in list(self.travel_data_attributes.keys()):
            has_category = logical_or(has_category, agent_category_attr==k)
        missing_category = where(logical_not(has_category))
        if missing_category[0].size > 0:
            logger.log_warning("attribute for agents category at index %s are not in travel data; value set to %s." % ( str(missing_category), self.default_value) )

        return results
