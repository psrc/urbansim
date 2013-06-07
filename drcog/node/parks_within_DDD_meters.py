# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import zeros

class parks_within_DDD_meters(Variable):
    """
    """
    
    def __init__(self, distance):
        Variable.__init__(self)
        self.distance = distance
        
    def compute(self,  dataset_pool):
        nodes = dataset_pool.get_dataset('node')
        result = nodes.parks_query(self.distance)
        return result
