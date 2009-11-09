# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.functions import attribute_label
from opus_core.variables.variable import Variable
from numpy import array, where, float32, zeros
from scipy.ndimage import sum as ndimage_sum
from psrc.opus_package_info import package

from opus_core.tests import opus_unittest

class AbstractTripMode(Variable):
    """
    Calculates a mode split of a particular subset of modes over a different subset.
    """
    _return_type = "float32"
    def __init__(self, matrices):
        self.matrices = ["psrc.travel_data.%s" % m for m in matrices]
        Variable.__init__(self)
        
    def dependencies(self):
        return self.matrices
    
    def compute(self, dataset_pool):
        zone_set = self.get_dataset()
        travel_data = dataset_pool.get_dataset('travel_data')
        from_zone_id = travel_data.get_attribute('from_zone_id')
        zone_ids = zone_set.get_attribute('zone_id')
        
        results = zeros(len(zone_ids)).astype(float32)
        for matrix in self.matrices:
            results += array(ndimage_sum(travel_data.get_attribute(matrix), labels = from_zone_id, index=zone_ids))
        return results
    