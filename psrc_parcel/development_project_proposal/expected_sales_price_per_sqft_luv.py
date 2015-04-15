# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import where, logical_not, logical_or, logical_and, zeros, ones
from opus_core.variables.variable import Variable
from opus_core.variables.functions import expfin
from opus_core.logger import logger
from ctypes.test import is_resource_enabled


class expected_sales_price_per_sqft_luv(Variable):
    """
    Exponentiated proposals' expected revenue per sqft used for LUV. 
    The base is 9% of the expected sales price per sqft. For fine-tuning we give some zones (TAZ or FAZ)
    an advantage or disadvantage. The numbers below determine the percentage. If it's above 9 it means
    those all proposals in those zones will have higher revenue than others. Below 9 means the opposite.
    """
    _return_type="float32"
        
    zone_based_weights = -1*ones((3701,2), dtype='float32')
    faz_based_weights = -1*ones((9917, 2), dtype='float32')
    res = 0
    nonres = 1
    zone_based_weights[[2598, 2657], res] = 15
    zone_based_weights[[2145, 2309], nonres] = 15
    zone_based_weights[[2151, 2286, 2293, 2481, 2475,  2116, 6316], res] = 18 # double increase
    zone_based_weights[[2172, 2127, 2284, 2570, 2520, 2487, 2554, 2249, 2169], nonres] = 18
    zone_based_weights[2147, nonres] = 27 # 3x increase
    zone_based_weights[[2145, 2309], nonres] = 36 # 4x increase
    zone_based_weights[[2311, 2310, 2312, 2121, 2282, 2257, 2409, 2171, 2597], nonres] = 4.5 # half decrease
    zone_based_weights[2214, res] = 1 # only 1% revenue 
    zone_based_weights[[2118, 2252, 2251, 2564], nonres] = 1
    
    faz_based_weights[705, res] = 18
    faz_based_weights[[505, 705, 6216], nonres] = 18
    faz_based_weights[5925, nonres] = 36
    faz_based_weights[[5825, 5915, 6114, 6115, 6125], nonres] = 1
    
        
    def dependencies(self):
        return ["development_project_proposal.expected_sales_price_per_sqft", 
                "urbansim_parcel.development_project_proposal.zone_id",
                "urbansim_parcel.development_project_proposal.faz_id",
                "is_res = development_project_proposal.aggregate(urbansim_parcel.development_project_proposal_component.is_residential) > 0"
                ]
    
    def compute(self,  dataset_pool):
        dpp = self.get_dataset()
        is_res = dpp['is_res']
        is_non_res = logical_not(is_res)
        wis_res = where(is_res)
        wis_non_res = where(is_non_res)
        rev = 9*ones(dpp.size(), dtype="float32")
        rev[wis_res] = self.faz_based_weights[dpp['faz_id'][wis_res], self.res]
        rev[wis_non_res] = self.faz_based_weights[dpp['faz_id'][wis_non_res], self.nonres]
        zone_rev = self.zone_based_weights[dpp['zone_id'][wis_res], self.res]
        where_weight = where(zone_rev >= 0)
        rev[wis_res][where_weight] = zone_rev[where_weight]
        zone_rev = self.zone_based_weights[dpp['zone_id'][wis_non_res], self.nonres]
        where_weight = where(zone_rev >= 0)
        rev[wis_non_res][where_weight] = zone_rev[where_weight]
        rev[where(rev < 0)] = 9    
        price = rev/100. * dpp["expected_sales_price_per_sqft"]
        return expfin(price)
