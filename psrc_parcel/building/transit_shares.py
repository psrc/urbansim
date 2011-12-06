# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from numpy import arange, zeros, array, where

class transit_shares(Variable):
    """ This variable is to be used to compute correction weights in the WESML estimation procedure.
    It computes shares W_g/H_g as defined in Ben-Akiva & Lermann (p.238, Eq 8.34) where g is a building.
    It is using the expansion factor from the household survey which has different factors for
    households living in five different areas each of which is divided into an out of transit area and 
    in transit area. The numbers are taken from the PSRC 2006 Household Activity Survey Analysis Report, page E-3.
    """
    _return_type = "float32"

    # expansion factor from household survey 
    #                Seattle  King    Snoh    Pierce  Kitsap
    weights = array([[223.13, 404.58, 364.77, 460.91, 159.16], # out of transit area
                     [187.38, 359.14, 303.71, 335.88, 160.12 ]]) # in transit area
    # number of records in the estimation dataset per area
    number_hh_est = array([[134, 766, 566, 572, 593], # out of transit area
                           [1275, 523, 189, 95, 26]]) # in transit area
    # number of records in the household survey per area
    number_hh_survey = array([[6917, 308692, 194788, 250733, 91674], # out of transit area
                              [254457, 175978, 59223, 32244, 2722]]) # in transit area
    total_transit_est = float(number_hh_est.sum())
    total_transit_observed = (weights*number_hh_survey).sum()
    W = (weights*number_hh_survey)/total_transit_observed
    H = number_hh_est/total_transit_est
    share_ratio = W/H
    
    # dictionary that assigns large area ids to the five areas above
    la_area = {
        0: [6],             # Seattle
        1: [5,7,8,9,10,11], # rest King 
        2: [1,2,3,4],       # Snohomish
        3: [12,13,14,15],   # Pierce
        4: [16,17,18]       # Kitsap
    }
    def dependencies(self):
        return ["urbansim_parcel.building.large_area_id", 
                "is_in_transit_zone = building.disaggregate(parcel.is_in_transit_zone)"]

    def compute(self,  dataset_pool):
        ds = self.get_dataset()
        result = zeros(ds.size())

        for group in arange(5):
            large_areas = zeros(ds.size(), dtype='bool8')
            which_la = self.la_area[group]
            for la in which_la:
                large_areas[ds["large_area_id"]==la] = True
            for inout in [0,1]:
                idx = (ds["is_in_transit_zone"] == inout)*large_areas
                result[where(idx)] = self.share_ratio[inout, group]
        return result
    