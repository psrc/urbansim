# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.functions import attribute_label
from opus_core.variables.variable import Variable
from numpy import array, where, float32, zeros
from scipy.ndimage import sum as ndimage_sum
from psrc.opus_package_info import package

from opus_core.tests import opus_unittest

class AbstractModeSplit(Variable):
    """
    Calculates a mode split of a particular subset of modes over a different subset.
    """
    _return_type = "float32"
    def __init__(self, numerator_modes, denominator_modes, path = 'psrc.zone'):
        self.path = path
        self.numerator_modes = numerator_modes
        self.denominator_modes = denominator_modes                     
        Variable.__init__(self)
        
    def dependencies(self):
        dep = ["%s.%s" % (self.path, mode) for mode in self.numerator_modes]
        for mode in self.denominator_modes:
            if not mode in dep:
                dep.append("%s.%s" % (self.path,mode))
        return dep
    
    def compute(self, dataset_pool):
        zone_set = self.get_dataset()
        zone_ids = zone_set.get_attribute('zone_id')
        
        numerator = zeros(len(zone_ids)).astype(float32)
        for mode in self.numerator_modes:
            numerator += ndimage_sum(zone_set.get_attribute(mode), labels = zone_ids, index=zone_ids)
        denominator = zeros(len(zone_ids)).astype(float32)
        for mode in self.denominator_modes:
            denominator += ndimage_sum(zone_set.get_attribute(mode), labels = zone_ids, index=zone_ids)
                
        """if there is a divide by zero then replace with 1"""
        denominator[where(denominator == 0)] = 1

        return numerator / denominator
