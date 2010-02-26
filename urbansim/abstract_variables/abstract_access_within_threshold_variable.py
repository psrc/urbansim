# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.logger import logger
from opus_core.variables.variable import Variable
from numpy import array, newaxis

class abstract_access_within_threshold_variable(Variable):
    """abstract variable for access to zone attribute within a given threshold, 
    e.g. employment_within_30_minutes_travel_time_hbw_am_transit_walk.
    This is a variable for zone dataset
    """

    from_origin = True
    _return_type = "int32"
    threshold = "to_be_defined"
    travel_data_attribute  = "to_be_defined_in_fully_qualified_name"
    zone_attribute_to_access = "to_be_defined_in_fully_qualified_name"
    function = "sum"  #available functions: mean, minimum, maximum, variance
    
    def dependencies(self):
        return [self.travel_data_attribute,
                self.zone_attribute_to_access]

    def compute(self, dataset_pool):
        travel_data = dataset_pool.get_dataset('travel_data')
        zones = dataset_pool.get_dataset('zone')
        
        zone_ids = zones.get_id_attribute()
        zone_attribute = zones.get_attribute(self.zone_attribute_to_access)
        travel_data_attribute_mat = travel_data.get_attribute_as_matrix(self.travel_data_attribute, fill=self.threshold+1)
        
        if self.from_origin:
            vv = (travel_data_attribute_mat <= self.threshold)[:, zone_ids] * zone_attribute[newaxis,:]            
            results = vv.sum(axis=1)[zone_ids]
        else:
            vv = (travel_data_attribute_mat <= self.threshold)[zone_ids, :] * zone_attribute[:, newaxis]            
            results = vv.sum(axis=0)[zone_ids]
        
        return results

## unittest in child classes