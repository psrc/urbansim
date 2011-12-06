# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from numpy import arange, zeros, array, where

class transit_shares(Variable):
    _return_type = "float32"

    la_array = zeros((5, 19), dtype='bool8')
    la_array[0, 6] = True # Seattle
    la_array[1, [5,7,8,9,10,11]] = True # rest King 
    la_array[2, arange(1,5)] = True # Snohomish
    la_array[3, arange(12,16)] = True # Pierce
    la_array[4, arange(16,19)] = True # Kitsap
    weights = array([[223.13, 404.58, 364.77, 460.91, 159.16], [187.38, 359.14, 303.71, 335.88, 160.12 ]])
    number_hh_est = array([[134, 766, 566, 572, 593], [1275, 523, 189, 95, 26]])
    number_hh_survey = array([[6917, 308692, 194788, 250733, 91674],[254457, 175978, 59223, 32244, 2722]])
    total_transit_est = float(number_hh_est.sum())
    total_transit_observed = (weights*number_hh_survey).sum()
    W = (weights*number_hh_survey)/total_transit_observed
    H = number_hh_est/total_transit_est
    share_ratio = W/H
    def dependencies(self):
        return ["urbansim_parcel.building.large_area_id", 
                "is_in_transit_zone = building.disaggregate(parcel.is_in_transit_zone)"]

    def compute(self,  dataset_pool):
        ds = self.get_dataset()
        result = zeros(ds.size())

        for group in arange(5):
            large_areas = zeros(ds.size(), dtype='bool8')
            which_la = where(self.la_array[group,:])[0]
            for la in which_la:
                large_areas[ds["large_area_id"]==la] = True
            for inout in [0,1]:
                idx = (ds["is_in_transit_zone"] == inout)*large_areas
                result[where(idx)] = self.share_ratio[inout, group]
        return result