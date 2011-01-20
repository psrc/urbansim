# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.logger import logger
from opus_core.variables.variable import Variable
from opus_core.variables.variable_name import VariableName
from numpy import where, power, float32, array
from opus_core import ndimage
from opus_core.misc import safe_array_divide

class abstract_weighted_access(Variable):
    """
    Summarizes zone attribute weighted by a travel_data attribute, e.g. 
    generalized_cost_weighted_access_to_employment_hbw_am_drive_alone = 
    sum of number of jobs in zone j divided by generalized cost from zone i to j,
    The weight is the home-based-work am generalized cost by auto drive-alone.
    """

    #_return_type = "int32"    
    aggregate_by_origin = True    
    #whether aggregate by origin zone or destination zone
    travel_data_attribute  = "to_be_defined_in_fully_qualified_name"
    ## weight = 1 / power(travel_data_attribute, 2)
    zone_attribute_to_access = "to_be_defined_in_fully_qualified_name"
    function = "sum"  #available functions: mean, minimum, maximum, variance
    default_package_order = ["urbansim", "opus_core"]
        
    def dependencies(self):
        return [self.travel_data_attribute,
                self.zone_attribute_to_access]
       
    def compute(self,  dataset_pool):
        zones = self.get_dataset()
        zone_ids = zones.get_id_attribute()
        travel_data = dataset_pool.get_dataset("travel_data")
#        import ipdb; ipdb.set_trace()
        if self.aggregate_by_origin:
            attribute_zone_id = travel_data.get_attribute("from_zone_id")
            summary_zone_id = travel_data.get_attribute("to_zone_id")
        else:
            attribute_zone_id = travel_data.get_attribute("to_zone_id")
            summary_zone_id = travel_data.get_attribute("from_zone_id")
            
        zone_index = zones.get_id_index(attribute_zone_id)
        attribute = zones[self.zone_attribute_to_access][zone_index]
        weight = safe_array_divide(1.0, 
                            power(travel_data[self.travel_data_attribute],2))
        
        function = getattr(ndimage, self.function)
        results = array(function(attribute * weight, 
                                 labels = summary_zone_id, 
                                 index=zone_ids))
        
        return results

## unittests in child class