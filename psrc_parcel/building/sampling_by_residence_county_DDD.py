# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import where, ones, logical_not
from opus_core.variables.variable import Variable

class sampling_by_residence_county_DDD(Variable):

    def __init__(self, county_id):
        self.county_id = county_id
        Variable.__init__(self)
        
    def dependencies(self):
        return ["urbansim_parcel.building.county_id", "urbansim_parcel.building.vacant_residential_units"]
    
    def compute(self, dataset_pool):
        ds = self.get_dataset()
        vacant = (ds["vacant_residential_units"]>0).sum()
        this_area = ds['county_id'] == self.county_id
        result = ones(ds.size()).astype('float32')
        if (ds["vacant_residential_units"][where(this_area)]>0).sum() > 0:
            result[where(logical_not(this_area))] = 0
        return result
        