# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import zeros
import numpy

class transit_type_DDD_within_DDD_meters(Variable):
    """
    """
    
    def __init__(self, cat, distance):
        Variable.__init__(self)
        self.category = cat
        self.distance = distance
        
    def compute(self,  dataset_pool):
        nodes = dataset_pool.get_dataset('node')
        result = nodes.transit_dist_query(self.distance,self.category)
        result = numpy.array(result,dtype=numpy.float32)
        result = numpy.array(result < self.distance,dtype=int)
        return result
