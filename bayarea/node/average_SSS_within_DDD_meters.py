# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import zeros

class average_SSS_within_DDD_meters(Variable):
    """
    """
    
    def __init__(self, attribute, distance):
        Variable.__init__(self)
        self.attribute = attribute
        self.distance = distance
        
    def compute(self,  dataset_pool):
        nodes = dataset_pool.get_dataset('node')
        result = nodes.building_avg_query(self.distance, self.attribute)
        return result
