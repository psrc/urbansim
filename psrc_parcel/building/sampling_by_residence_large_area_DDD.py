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
        return ["urbansim_parcel.building.large_area_id", "urbansim_parcel.building.vacant_residential_units"]
    
    def compute(self, dataset_pool):
        ds = self.get_dataset()
        vacant = (ds["vacant_residential_units"]>0).sum()
        this_area_index = where(ds['large_area_id'] == self.large_area_id)[0]
        vacant_this_area = (ds["vacant_residential_units"][this_area_index]>0).sum()
        result = zeros(ds.size()).astype('float32')
        if vacant-vacant_this_area > 0:
            result[:] = 60.0/(vacant-vacant_this_area)
        if vacant_this_area > 0:
            result[this_area_index] = 40.0/vacant_this_area
        return result
        