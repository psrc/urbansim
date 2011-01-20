# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.logger import logger
from opus_core.variables.variable import Variable
from numpy import zeros, float32

class abstract_travel_time_variable_for_non_interaction_dataset(Variable):
    """ Return travel data attribute for specified zone pairs for a single non-interaction dataset
    use  abstract_travel_time_variable for interaction dataset
    """
    
    default_value = 999
    origin_zone_id = 'to_be_defined_in_fully_qualified_name'
    destination_zone_id = 'to_be_defined_in_fully_qualified_name'
    travel_data_attribute = 'to_be_defined_in_fully_qualified_name'

    def dependencies(self):
        return [ self.origin_zone_id, 
                self.destination_zone_id, 
                self.travel_data_attribute]
    
    def compute(self, dataset_pool):
        dataset = self.get_dataset()
        origin_zones = dataset.get_attribute(self.origin_zone_id)
        destination_zones = dataset.get_attribute(self.destination_zone_id)
        
        travel_data = dataset_pool.get_dataset('travel_data')
        travel_data_attr_mat = travel_data.get_attribute_as_matrix(self.travel_data_attribute, 
                                                                   fill=self.default_value)
        results = travel_data_attr_mat[origin_zones, destination_zones]
        
        missing_pairs_index = travel_data.get_od_pair_index_not_in_dataset(origin_zones, destination_zones)
        if missing_pairs_index[0].size > 0:
            results[missing_pairs_index] = self.default_value
            logger.log_warning("zone pairs at index %s are not in travel data; value set to %s." % ( str(missing_pairs_index), self.default_value) )
        
        return results

##unittest in child class