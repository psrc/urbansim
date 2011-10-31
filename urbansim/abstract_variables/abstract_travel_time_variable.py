# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import where, repeat, ones, float32, resize, array
from numpy import ma
from urbansim.functions import attribute_label
from opus_core.logger import logger

class abstract_travel_time_variable(Variable):
    """abstract variable for bunch of interaction travel time variables"""

    default_value = 180.0
    agent_zone_id = 'to_be_defined_in_fully_qualified_name'
    location_zone_id = 'to_be_defined_in_fully_qualified_name'
    travel_data_attribute = 'to_be_defined_in_fully_qualified_name'
    direction_from_home = True

    def dependencies(self):
        return [ self.agent_zone_id, self.location_zone_id, self.travel_data_attribute]

    def compute(self, dataset_pool):
        interaction_dataset = self.get_dataset()
        travel_data = dataset_pool.get_dataset('travel_data')
        travel_data_attr_mat = travel_data.get_attribute_as_matrix(self.travel_data_attribute, 
                                                                   fill=self.default_value)
        
        zone1 = interaction_dataset.get_dataset(1).get_attribute_by_index(self.agent_zone_id,
                                                                      interaction_dataset.get_2d_index_of_dataset1())
        zone2 = interaction_dataset.get_2d_dataset_attribute(self.location_zone_id)
        if self.direction_from_home:
            home_zone = zone1.astype("int32")
            work_zone = zone2.astype("int32")
        else:
            home_zone = zone2.astype("int32")
            work_zone = zone1.astype("int32")
        
        results = resize(array([self.default_value], dtype=float32), home_zone.shape)
        results = travel_data_attr_mat[home_zone, work_zone]
        
        missing_pairs_index = travel_data.get_od_pair_index_not_in_dataset(home_zone, work_zone)
        if missing_pairs_index[0].size > 0:
            results[missing_pairs_index] = self.default_value
            logger.log_warning("zone pairs %s are not in travel data; value set to %s." % ( zip(home_zone[missing_pairs_index], work_zone[missing_pairs_index]), self.default_value) )
            logger.log_warning("Values for %s O-D pairs in %s interaction dataset reset." % ( missing_pairs_index[0].size, home_zone.shape ) )
        
        return results
