# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import where, zeros
from opus_core.variables.variable import Variable

class sampling_by_residence_large_area_DDD(Variable):

    def __init__(self, large_area_id):
        self.large_area_id = large_area_id
        Variable.__init__(self)
        
    def dependencies(self):
        return ["psrc_parcel.school.large_area_id"]
    
    def compute(self, dataset_pool):
        ds = self.get_dataset()
        this_area_index = where(ds['large_area_id'] == self.large_area_id)[0]
        result = zeros(ds.size()).astype('float32')
        result[:] = 20.0 / float(ds.size() - this_area_index.size)
        if this_area_index.size > 0:
            result[this_area_index] = 80.0/float(this_area_index.size)
        return result
        